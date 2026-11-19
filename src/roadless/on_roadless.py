"""Roadless-area metrics for Ontario from ORN Road Net Element plus MNR Road Segments.

The paper analysed the Ontario Road Network (ORN, MTO) and the MNR road
segments (resource access, forest and park roads) separately and summed them;
the buffer union here makes the overlap harmless. Both layers come from the LIO
open-data ArcGIS service as GeoPackages (`fetch_inputs.py arcgis`, see
`fetch_inputs_on()`), under the Open Government Licence - Ontario.

Filter, default: drop ORN ROAD_ELEMENT_TYPE FERRY CONNECTION. Nothing is
dropped from MNR (the paper lists no ON exclusions, note 02). `--strict` also
drops ORN VIRTUAL ROAD (connectors across gaps) and MNR segments that are
destroyed, planted or Closed, as an upper bound on roadless area.
Usage: uv run python src/roadless/on_roadless.py [--strict]
Output: data/processed/on[_strict]/ontario/
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

from fetch_inputs import fetch_arcgis
from osm_roadless import CRS
from single_dataset import run

LIO = "https://ws.lioservices.lrc.gov.on.ca/arcgis2/rest/services/LIO_OPEN_DATA/LIO_Open09/MapServer"
ORN_LAYER, MNR_LAYER = f"{LIO}/0", f"{LIO}/18"
ORN_EXCLUDED = ["FERRY CONNECTION"]
ORN_STRICT_EXTRA = ["VIRTUAL ROAD"]


def fetch_inputs_on() -> tuple[Path, Path]:
    return fetch_arcgis(ORN_LAYER, "on_orn_roads"), fetch_arcgis(MNR_LAYER, "on_mnr_roads")


def load_roads(orn_path: Path, mnr_path: Path, strict: bool = False) -> gpd.GeoDataFrame:
    orn = gpd.read_file(orn_path, layer="roads", engine="pyogrio",
                        columns=["OGF_ID", "ROAD_ELEMENT_TYPE"])
    mnr = gpd.read_file(mnr_path, layer="roads", engine="pyogrio",
                        columns=["OGF_ID", "STATUS", "ROADBED_DESTROYED_IND", "ROADBED_PLANTED_IND"])
    orn = orn[~orn["ROAD_ELEMENT_TYPE"].isin(ORN_EXCLUDED + (ORN_STRICT_EXTRA if strict else []))]
    if strict:
        bad = (mnr["ROADBED_DESTROYED_IND"] == "Yes") | (mnr["ROADBED_PLANTED_IND"] == "Yes") \
            | (mnr["STATUS"] == "Closed")
        mnr = mnr[~bad]
    both = pd.concat([orn[["geometry"]].assign(source="ORN"), mnr[["geometry"]].assign(source="MNR")],
                     ignore_index=True)
    return gpd.GeoDataFrame(both, crs=orn.crs).to_crs(CRS)


def main(strict: bool) -> None:
    run("on_strict" if strict else "on", "Ontario", "ontario",
        lambda: load_roads(*fetch_inputs_on(), strict), strict=strict)


if __name__ == "__main__":
    main("--strict" in sys.argv)
