"""Roadless-area metrics for Nova Scotia from the NSTDB Roads, Trails and Rails (Road Line Layer).

The Nova Scotia Topographic Database layer the paper used (note 02), from the
Nova Scotia open data portal (resource a6gf-w68e, OGL-Nova Scotia; 336,702
features, includes tracks and resource access roads that the NRN lacks).
Download: `fetch_inputs.py socrata data.novascotia.ca a6gf-w68e ns_nstdb_roads`.

Filter on `feat_desc`, default = the paper's exclusions: DRIVEWAY, FERRY
CROSSING, FOOT BRIDGE, RAILROAD (line, overhead, ruin), TRAIL (three variants),
WALK, WATER ACCESS. `--strict` also drops BRIDGE - Driveway and Trail, TRACK -
Addressed Feature - No Vehicular Traffic, every Abandoned road or bridge, and
the RDTMP status-unknown placeholder, as an upper bound on roadless area.
Usage: uv run python src/roadless/ns_roadless.py [--strict]
Output: data/processed/ns[_strict]/nova-scotia/
"""
import sys
from pathlib import Path

import geopandas as gpd

from fetch_inputs import fetch_socrata
from osm_roadless import CRS
from single_dataset import run

EXCLUDED_PREFIX = ("DRIVEWAY", "FERRY", "FOOT BRIDGE", "RAILROAD", "TRAIL", "WALK", "WATER ACCESS")
STRICT_EXTRA_PREFIX = ("BRIDGE - Driveway", "BRIDGE - Trail", "TRACK - Addressed",
                       "ROAD - Abandoned", "BRIDGE - Abandoned")
STRICT_EXTRA_CODE = ("RDTMP",)


def load_roads(path: Path, strict: bool = False) -> gpd.GeoDataFrame:
    roads = gpd.read_file(path, layer="roads", engine="pyogrio")
    desc = roads["feat_desc"].fillna("")
    drop = desc.str.startswith(EXCLUDED_PREFIX)
    if strict:
        drop |= desc.str.startswith(STRICT_EXTRA_PREFIX) | roads["feat_code"].isin(STRICT_EXTRA_CODE)
    return roads[~drop].to_crs(CRS)


def main(strict: bool) -> None:
    run("ns_strict" if strict else "ns", "Nova Scotia", "nova-scotia",
        lambda: load_roads(fetch_socrata("data.novascotia.ca", "a6gf-w68e", "ns_nstdb_roads"), strict),
        strict=strict)


if __name__ == "__main__":
    main("--strict" in sys.argv)
