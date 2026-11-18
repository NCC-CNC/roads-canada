"""Roadless-area metrics from the National Road Network (NRN), one jurisdiction.

Same method as osm_roadless.py (1 km buffer, StatCan 2016 land mask); only the
road loader differs. This is the pattern for adding a provincial dataset: a
loader that returns vehicle roads in EPSG:3347, then the shared
`roadless_patches` and `summarize`.

NRN road class (ROADCLASS) is a functional class, so every ROADSEG feature is
a road for motor vehicles; ferries are in a separate layer that is not read.
Nothing is dropped by default, which matches the paper: the NT total with
Winter roads (7,173 km) is within 3% of the paper's NRN figure (7,401 km), and
without them (4,387 km) it is not. Pass `excluded=["Winter"]` to treat
ice and snow roads as non-permanent (they are 39% of NT NRN length).
Usage: uv run python src/roadless/nrn_roadless.py <nrn.gpkg> <boundary-file> <name>
"""
import sys
from pathlib import Path

import geopandas as gpd
import pyogrio

from osm_roadless import CRS, load_boundary, roadless_patches, summarize

EXCLUDED_ROADCLASS: list[str] = []


def load_roads(gpkg: Path, excluded=EXCLUDED_ROADCLASS) -> gpd.GeoDataFrame:
    layer = next(n for n, _ in pyogrio.list_layers(gpkg) if n.endswith("_ROADSEG"))
    roads = gpd.read_file(
        gpkg, layer=layer, engine="pyogrio",
        columns=["NID", "ROADCLASS", "PAVSTATUS", "CLOSING", "REVDATE"],
    )
    roads = roads[~roads["ROADCLASS"].isin(excluded)]
    return roads.to_crs(CRS)


def main(gpkg: str, boundary_path: str, name: str, out_dir: str = "data/processed") -> None:
    roads = load_roads(Path(gpkg))
    boundary = load_boundary(Path(boundary_path))
    patches = roadless_patches(roads, boundary)
    stats = summarize(patches, boundary.geometry.area.sum() / 1e6)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    patches.to_parquet(Path(out_dir) / f"roadless_patches_nrn_{name.replace(' ', '_')}.parquet")
    print(f"roads kept: {len(roads):,}, length km: {roads.length.sum() / 1000:,.0f}")
    for k, v in stats.items():
        print(f"{k}: {v:,.1f}" if isinstance(v, float) else f"{k}: {v}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
