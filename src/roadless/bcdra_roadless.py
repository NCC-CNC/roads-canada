"""Roadless-area metrics from the BC Digital Road Atlas (DRA), British Columbia.

Second dataset through the shared pipeline (after the NRN). Only the loader
and the class filter are DRA specific. Resource and low-use roads are in the
DRA, which the NRN largely lacks for BC.

Filter (`RD_CLASS`), default = the paper's exclusions (Supporting Information,
note 02): ferry, driveway (private driveway), pedestrian (pedestrian mall),
proposed, runway, water (water access). `--strict` also drops trail and roads
whose `RD_SURFACE` is decommissioned or rehabilitated, as an upper bound on
roadless area. Boundary is the shared StatCan 2016 mask.
Usage: uv run python src/roadless/bcdra_roadless.py [--strict]
Output: data/processed/bcdra[_strict]/british-columbia/ (stats.json, patches.parquet)
"""
import sys
from pathlib import Path

import geopandas as gpd

from fetch_inputs import fetch_bcdra
from osm_roadless import CRS
from single_dataset import run

LAYER = "DGTL_ROAD_ATLAS_MPAR_SP"
EXCLUDED_CLASS = ["ferry", "driveway", "pedestrian", "proposed", "runway", "water"]
STRICT_EXTRA_CLASS = ["trail"]
STRICT_EXTRA_SURFACE = ["decommissioned", "rehabilitated"]


def load_roads(gdb: Path, strict: bool = False) -> gpd.GeoDataFrame:
    roads = gpd.read_file(gdb, layer=LAYER, engine="pyogrio",
                          columns=["ID", "RD_CLASS", "FEAT_TYPE", "RD_SURFACE"])
    drop = EXCLUDED_CLASS + (STRICT_EXTRA_CLASS if strict else [])
    keep = ~roads["RD_CLASS"].isin(drop)
    if strict:
        keep &= ~roads["RD_SURFACE"].isin(STRICT_EXTRA_SURFACE)
    return roads[keep].to_crs(CRS)


def main(strict: bool) -> None:
    run("bcdra_strict" if strict else "bcdra", "British Columbia", "british-columbia",
        lambda: load_roads(fetch_bcdra(), strict), strict=strict)


if __name__ == "__main__":
    main("--strict" in sys.argv)
