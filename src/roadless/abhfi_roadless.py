"""Roadless-area metrics from the Alberta Human Footprint Inventory (ABMI HFI 2023).

Third dataset through the shared pipeline. Reads the road centerline layer
(`o03_Roads_Centerlines_HFI_2023`) only; the seismic lines, trails and other
linear features layer (4.2 million lines) is not roads and stays out.

Filter (`FEATURE_TY`), default = the paper's exclusion (note 02): AIRP-RUNWAY
(and RIS-AIRP-RUNWAY, the oil sands equivalent). `--strict` also drops
ROAD-VEGETATED, ROAD-VEGETATED-OSE (access dispositions with no detectable
road surface) and ROAD-WINTER, as an upper bound on roadless area.
Usage: uv run python src/roadless/abhfi_roadless.py [--strict]
Output: data/processed/abhfi[_strict]/alberta/
"""
import sys
from pathlib import Path

import geopandas as gpd

from fetch_inputs import fetch_abhfi
from osm_roadless import CRS
from single_dataset import run

LAYER = "o03_Roads_Centerlines_HFI_2023"
EXCLUDED_TYPE = ["AIRP-RUNWAY", "RIS-AIRP-RUNWAY"]
STRICT_EXTRA_TYPE = ["ROAD-VEGETATED", "ROAD-VEGETATED-OSE", "ROAD-WINTER"]


def load_roads(gdb: Path, strict: bool = False) -> gpd.GeoDataFrame:
    roads = gpd.read_file(gdb, layer=LAYER, engine="pyogrio",
                          columns=["FEATURE_TY", "SOURCE", "YEAR"])
    drop = EXCLUDED_TYPE + (STRICT_EXTRA_TYPE if strict else [])
    return roads[~roads["FEATURE_TY"].isin(drop)].to_crs(CRS)


def main(strict: bool) -> None:
    run("abhfi_strict" if strict else "abhfi", "Alberta", "alberta",
        lambda: load_roads(fetch_abhfi(), strict), strict=strict)


if __name__ == "__main__":
    main("--strict" in sys.argv)
