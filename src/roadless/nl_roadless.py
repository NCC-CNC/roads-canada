"""Roadless-area metrics for Newfoundland and Labrador: NRN plus Resource Access Roads.

Resource Access Roads (formerly Forest Access Roads) is maintained by the
Department of Fisheries, Forestry and Agriculture and published as two ArcGIS
Online feature services (FFA_ResourceRoads_NF layer 2, FFA_ResourceRoads_LB
layer 0; 12,431 and 1,049 features, 27,878 km, modified 2025-10-31), under the
Open Government Licence - Newfoundland and Labrador. The paper's merged
baseline used the same layer (downloaded January 2021, note 13).
The NRN supplies the public roads; the two overlap where the resource layer
touches public roads, which does not change the union buffer.

Default keeps every feature (the paper's baseline did too). `--strict` drops
roads rated ATV only or Not Passable (ROAD_ACCESS 3, 3_ATV, 4, 4_NotPassable),
as an upper bound on roadless area. Codes 1 to 6 appear in two styles; 5 and 6
(Unknown) are kept.
Download: see `fetch_inputs_nl()`.
Usage: uv run python src/roadless/nl_roadless.py [--strict]
Output: data/processed/nl[_strict]/newfoundland-and-labrador/
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

from fetch_inputs import fetch_arcgis, fetch_nrn
from nrn_roadless import load_roads as load_nrn
from osm_roadless import CRS
from single_dataset import run

SVC = "https://services8.arcgis.com/aCyQID5qQcyrJMm2/arcgis/rest/services"
STRICT_DROP_ACCESS = ["3", "3_ATV", "4", "4_NotPassable"]


def fetch_inputs_nl() -> tuple[Path, Path, Path]:
    return (fetch_nrn("NL"),
            fetch_arcgis(f"{SVC}/FFA_ResourceRoads_NF/FeatureServer/2", "nl_resource_roads_nf"),
            fetch_arcgis(f"{SVC}/FFA_ResourceRoads_LB/FeatureServer/0", "nl_resource_roads_lb"))


def load_roads(nrn: Path, nf: Path, lb: Path, strict: bool = False) -> gpd.GeoDataFrame:
    res = pd.concat([gpd.read_file(p, layer="roads", engine="pyogrio", columns=["ROAD_ACCESS"]).to_crs(CRS)
                     for p in (nf, lb)], ignore_index=True)
    if strict:
        res = res[~res["ROAD_ACCESS"].isin(STRICT_DROP_ACCESS)]
    public = load_nrn(nrn)[["geometry"]]
    both = pd.concat([public.assign(source="nrn"), res[["geometry"]].assign(source="resource")],
                     ignore_index=True)
    return gpd.GeoDataFrame(both, crs=CRS)


def main(strict: bool) -> None:
    run("nl_strict" if strict else "nl", "Newfoundland and Labrador", "newfoundland-and-labrador",
        lambda: load_roads(*fetch_inputs_nl(), strict), strict=strict)


if __name__ == "__main__":
    main("--strict" in sys.argv)
