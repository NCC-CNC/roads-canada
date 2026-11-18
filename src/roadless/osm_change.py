"""Prototype: roadless-area change between two OSM snapshots (issue #5).

Runs the Poley et al. (2022) method on an old and a new Geofabrik snapshot,
then diffs them. Also tests the incremental shortcut: instead of rebuilding
from scratch, buffer only roads whose osm_id is new and subtract that from the
old roadless patches. The two routes should agree.
Usage: uv run python src/roadless/osm_change.py <old.shp.zip> <new.shp.zip> <boundary-file> <name>
"""
import sys
from pathlib import Path

import geopandas as gpd

from osm_roadless import BUFFER_M, CRS, load_boundary, load_roads, roadless_patches


def main(old_zip: str, new_zip: str, boundary_path: str, name: str, out_dir: str = "data/processed") -> None:
    boundary = load_boundary(Path(boundary_path))
    old_roads, new_roads = load_roads(Path(old_zip)), load_roads(Path(new_zip))
    old_patches = roadless_patches(old_roads, boundary)
    new_patches = roadless_patches(new_roads, boundary)

    old_ids, new_ids = set(old_roads["osm_id"]), set(new_roads["osm_id"])
    added = new_roads[~new_roads["osm_id"].isin(old_ids)]
    removed = old_roads[~old_roads["osm_id"].isin(new_ids)]

    # Incremental route: subtract buffered added roads from the old patches.
    old_union = old_patches.geometry.union_all()
    incr = old_union.difference(added.geometry.buffer(BUFFER_M).union_all())
    incr_area = incr.area / 1e6
    full_area = new_patches["area_km2"].sum()

    # Where new roads went: share of added length inside old roadless land.
    inside = added.geometry.intersection(old_union).length.sum()
    total = added.geometry.length.sum()
    # Added segments that opened roadless land, by size of the old patch hit.
    hit = gpd.sjoin(added[["geometry"]], old_patches[["area_km2", "geometry"]], predicate="intersects")
    big = hit[hit["area_km2"] >= 100]

    old_a, new_a = old_patches["area_km2"].sum(), full_area
    print(f"roads old/new: {len(old_roads):,} / {len(new_roads):,}")
    print(f"osm_id added: {len(added):,} ({total/1e3:,.0f} km), removed: {len(removed):,}")
    print(f"added road length inside old roadless land: {inside/1e3:,.0f} km ({100*inside/total:.1f}%)")
    print(f"added ways touching old patches >= 100 km2: {big.index.nunique():,}")
    print(f"roadless km2 old: {old_a:,.0f}  new (full): {new_a:,.0f}  change: {new_a-old_a:+,.0f}")
    print(f"patches old: {len(old_patches):,}  new: {len(new_patches):,}")
    print(f"roadless km2 new (incremental, added roads only): {incr_area:,.0f}  diff vs full: {incr_area-full_area:+,.1f}")

    # Roadless land lost, as polygons for mapping.
    lost = gpd.GeoDataFrame(geometry=[old_union.difference(new_patches.geometry.union_all())], crs=CRS)
    lost = lost.explode(index_parts=False).reset_index(drop=True)
    lost["area_km2"] = lost.geometry.area / 1e6
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    lost.to_parquet(Path(out_dir) / f"roadless_lost_{name.replace(' ', '_')}.parquet")
    print(f"lost polygons: {len(lost):,}, total {lost['area_km2'].sum():,.0f} km2")


if __name__ == "__main__":
    main(*sys.argv[1:5])
