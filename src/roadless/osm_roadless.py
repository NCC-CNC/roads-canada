"""Prototype: OSM roadless-area metrics for one jurisdiction.

Method follows Poley et al. (2022): drop OSM non-vehicle classes, buffer the
remaining roads by 1 km, and treat land outside the buffer as roadless.
Usage: uv run python src/roadless/osm_roadless.py <geofabrik.shp.zip> <boundary-file> <name>
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np

# Paper's OSM exclusion list (Supporting Information); everything else stays in.
EXCLUDED_FCLASS = ["bridleway", "cycleway", "footway", "path", "pedestrian", "steps"]
BUFFER_M = 1000
CRS = "EPSG:3347"  # Statistics Canada Lambert
SIZE_BINS_KM2 = [0, 10, 100, 1_000, 10_000, 100_000, np.inf]


def load_roads(shp_zip: Path) -> gpd.GeoDataFrame:
    roads = gpd.read_file(f"zip://{shp_zip}!gis_osm_roads_free_1.shp", engine="pyogrio")
    roads = roads[~roads["fclass"].isin(EXCLUDED_FCLASS)]
    return roads.to_crs(CRS)


def load_boundary(path: Path) -> gpd.GeoDataFrame:
    """Land boundary for one jurisdiction, any OGR-readable file."""
    return gpd.read_file(path, engine="pyogrio").to_crs(CRS)


def roadless_patches(roads: gpd.GeoDataFrame, boundary: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    land = boundary.geometry.union_all()
    buffered = roads.geometry.buffer(BUFFER_M).union_all()
    remaining = land.difference(buffered)
    patches = gpd.GeoDataFrame(geometry=[remaining], crs=CRS).explode(index_parts=False)
    patches["area_km2"] = patches.geometry.area / 1e6
    return patches.reset_index(drop=True)


def summarize(patches: gpd.GeoDataFrame, land_km2: float) -> dict:
    a = patches["area_km2"]
    out = {
        "land_km2": land_km2,
        "roadless_km2": a.sum(),
        "pct_roadless": 100 * a.sum() / land_km2,
        "patches": len(a),
        "mean_km2": a.mean(),
        "median_km2": a.median(),
        "max_km2": a.max(),
    }
    counts = np.histogram(a, bins=SIZE_BINS_KM2)[0]
    for lo, hi, n in zip(SIZE_BINS_KM2[:-1], SIZE_BINS_KM2[1:], counts):
        out[f"patches_{lo:g}_to_{hi:g}_km2"] = int(n)
    return out


def main(shp_zip: str, boundary_path: str, name: str, out_dir: str = "data/processed") -> None:
    roads = load_roads(Path(shp_zip))
    boundary = load_boundary(Path(boundary_path))
    patches = roadless_patches(roads, boundary)
    stats = summarize(patches, boundary.geometry.area.sum() / 1e6)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    patches.to_parquet(Path(out_dir) / f"roadless_patches_{name.replace(' ', '_')}.parquet")
    print(f"roads kept: {len(roads):,}")
    for k, v in stats.items():
        print(f"{k}: {v:,.1f}" if isinstance(v, float) else f"{k}: {v}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
