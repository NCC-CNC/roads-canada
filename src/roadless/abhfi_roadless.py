"""Roadless-area metrics from the Alberta Human Footprint Inventory (ABMI HFI 2023).

Third dataset through the shared pipeline. Reads the road centerline layer
(`o03_Roads_Centerlines_HFI_2023`) only; the seismic lines, trails and other
linear features layer (4.2 million lines) is not roads and stays out.

Filter (`FEATURE_TY`), default = the paper's exclusion (note 02): AIRP-RUNWAY
(and RIS-AIRP-RUNWAY, the oil sands equivalent). `--strict` also drops
ROAD-VEGETATED, ROAD-VEGETATED-OSE (access dispositions with no detectable
road surface) and ROAD-WINTER, as an upper bound on roadless area.
Usage: uv run python src/roadless/abhfi_roadless.py [--strict] [--2018]
Output: data/processed/abhfi[2018][_strict]/alberta/

`--2018` runs the 2018 edition the paper used (layer `o03_Roads_Centerlines_HFI2018`).
It has no ROAD-VEGETATED types, so strict drops the winter types only.
"""
import sys
from pathlib import Path

import geopandas as gpd

from fetch_inputs import fetch_abhfi, fetch_abhfi_2018
from osm_roadless import CRS
from single_dataset import run

LAYER = "o03_Roads_Centerlines_HFI_2023"
EXCLUDED_TYPE = ["AIRP-RUNWAY", "RIS-AIRP-RUNWAY"]
STRICT_EXTRA_TYPE = ["ROAD-VEGETATED", "ROAD-VEGETATED-OSE", "ROAD-WINTER"]

LAYER_2018 = "o03_Roads_Centerlines_HFI2018"
STRICT_EXTRA_TYPE_2018 = ["ROAD-WINTER-ACCESS", "ROAD-WINTER-ROAD", "FORD-WINTER-XING"]


def load_roads(gdb: Path, strict: bool = False, edition: str = "2023") -> gpd.GeoDataFrame:
    old = edition == "2018"
    roads = gpd.read_file(gdb, layer=LAYER_2018 if old else LAYER, engine="pyogrio",
                          columns=["FEATURE_TY", "SOURCE", "YEAR"])
    extra = STRICT_EXTRA_TYPE_2018 if old else STRICT_EXTRA_TYPE
    drop = EXCLUDED_TYPE + (extra if strict else [])
    return roads[~roads["FEATURE_TY"].isin(drop)].to_crs(CRS)


def main(strict: bool, edition: str = "2023") -> None:
    fetch = fetch_abhfi_2018 if edition == "2018" else fetch_abhfi
    label = "abhfi" + ("2018" if edition == "2018" else "") + ("_strict" if strict else "")
    run(label, "Alberta", "alberta",
        lambda: load_roads(fetch(), strict, edition), strict=strict, edition=edition)


if __name__ == "__main__":
    main("--strict" in sys.argv, "2018" if "--2018" in sys.argv else "2023")
