"""Roadless-area metrics for Yukon from the Yukon Road Network plus Forest Resource Roads 50k.

Both layers are GeoYukon ArcGIS services (Government of Yukon):
GY_Transportation layer 60 (Yukon Road Network, 8,164 km) and GY_Forestry
layer 39 (Forest Resource Roads - 50k, 595 km). Licence not verified (other
Yukon data use OGL-Yukon, note 02). Download: see `fetch_inputs_yt()`.

Default keeps every feature (the paper lists no Yukon exclusions). `--strict`
drops Road Network Winter and Driveway types and Forest Resource Roads of class
Trail, as an upper bound on roadless area.
Usage: uv run python src/roadless/yt_roadless.py [--strict]
Output: data/processed/yt[_strict]/yukon/
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

from fetch_inputs import fetch_arcgis
from osm_roadless import CRS
from single_dataset import run

GY = "https://mapservices.gov.yk.ca/arcgis/rest/services/GeoYukon"
NETWORK_LAYER, FOREST_LAYER = f"{GY}/GY_Transportation/MapServer/60", f"{GY}/GY_Forestry/MapServer/39"
STRICT_NETWORK_TYPES = ["Winter", "Driveway"]
STRICT_FOREST_CLASSES = ["Trail"]


def fetch_inputs_yt() -> tuple[Path, Path]:
    return fetch_arcgis(NETWORK_LAYER, "yt_road_network"), fetch_arcgis(FOREST_LAYER, "yt_forest_resource_roads")


def load_roads(network_path: Path, forest_path: Path, strict: bool = False) -> gpd.GeoDataFrame:
    net = gpd.read_file(network_path, layer="roads", engine="pyogrio", columns=["ROAD_TYPE"])
    forest = gpd.read_file(forest_path, layer="roads", engine="pyogrio", columns=["ROAD_CLASS"])
    if strict:
        net = net[~net["ROAD_TYPE"].isin(STRICT_NETWORK_TYPES)]
        forest = forest[~forest["ROAD_CLASS"].isin(STRICT_FOREST_CLASSES)]
    both = pd.concat([net[["geometry"]].assign(source="network"),
                      forest[["geometry"]].assign(source="forest")], ignore_index=True)
    return gpd.GeoDataFrame(both, crs=net.crs).to_crs(CRS)


def main(strict: bool) -> None:
    run("yt_strict" if strict else "yt", "Yukon", "yukon",
        lambda: load_roads(*fetch_inputs_yt(), strict), strict=strict)


if __name__ == "__main__":
    main("--strict" in sys.argv)
