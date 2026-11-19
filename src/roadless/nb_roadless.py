"""Roadless-area metrics for New Brunswick: NBRN public roads plus Forest Roads.

Two Government of New Brunswick layers, both under the New Brunswick Open
Government Licence:
- New Brunswick Road Network (NBRN, v10.2 file geodatabase from GeoNB; 66,865
  road segments, 31,362 km, includes a few Crown-land resource road classes).
  Ferries are a separate layer and are not read.
- Forest Roads (Socrata udwq-sw5i on gnb.socrata.com; 181,432 features), roads
  not maintained by the transportation department whose main purpose is access
  to forest resources. It has geometry only: no class, status or date, so
  nothing can be filtered.
Download: `fetch_nbrn()` and `fetch_socrata gnb.socrata.com udwq-sw5i nb_forest_roads`.

The two overlap where the NBRN holds resource roads; the union buffer is
unaffected, but `road_km` double counts that overlap. The paper used no
provincial NB dataset (Table 2: GRIP, gROADS, OSM, SC, NRN only).
Usage: uv run python src/roadless/nb_roadless.py
Output: data/processed/nb/new-brunswick/
"""
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

from fetch_inputs import RAW, download, fetch_socrata
from osm_roadless import CRS
from single_dataset import run

NBRN_URL = "https://geonb.snb.ca/downloads/nbrn/geonb_nbrn-rrnb_fgdb.zip"


def fetch_nbrn() -> Path:
    """NBRN file geodatabase (current edition only) to data/raw/nbrn/; returns the .gdb."""
    gdb = RAW / "nbrn" / "geonb_nbrn-rrnb_fgdb.gdb"
    if not gdb.exists():
        z = download(NBRN_URL, RAW / "nbrn" / "nbrn.zip")
        with zipfile.ZipFile(z) as f:
            f.extractall(RAW / "nbrn")
    return gdb


def load_roads(gdb: Path, forest: Path) -> gpd.GeoDataFrame:
    nbrn = gpd.read_file(gdb, layer="RoadSegmentEntity", engine="pyogrio", columns=[])
    fr = gpd.read_file(forest, layer="roads", engine="pyogrio", columns=[])
    both = pd.concat([nbrn[["geometry"]].to_crs(CRS).assign(source="nbrn"),
                      fr[["geometry"]].to_crs(CRS).assign(source="forest")], ignore_index=True)
    return gpd.GeoDataFrame(both, crs=CRS)


def main() -> None:
    run("nb", "New Brunswick", "new-brunswick",
        lambda: load_roads(fetch_nbrn(), fetch_socrata("gnb.socrata.com", "udwq-sw5i", "nb_forest_roads")))


if __name__ == "__main__":
    main()
