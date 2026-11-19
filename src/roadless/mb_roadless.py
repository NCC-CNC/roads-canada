"""Roadless-area metrics for Manitoba: NRN, MLI 1:20,000 transportation lines and BEAD roads.

The three sources the paper's merged baseline used for Manitoba (note 13):
- NRN, public roads.
- Manitoba Land Initiative Digital Topographic 1:20,000 transportation lines
  (trn_bas_20k_ln, 522,373 lines, 171,317 km; OpenMB licence). Photogrammetric
  from 1:60,000 photography, files dated 2009, and MLI stopped updating in
  February 2022, so this is a fixed edition.
  Download: https://mli.gov.mb.ca/t20k/shp_zip_files/trn_bas_20k_ln_shp.zip
- ECCC BEAD roads (Landsat-interpreted, 2015 edition via `bead.py`), which the
  paper added to fill the boreal north where the MLI layer is thin.

Default drops the non-road F_TYPE values (rail lines, footpaths and trails,
boardwalks, pedestrian bridges, snowmobile and portage trails) and keeps cart
tracks and accessways, as the paper's baseline did (it classed them as track).
`--strict` also drops CART TRACK, ACCESSWAY, BACK LANE and ROAD - U/C, as an
upper bound on roadless area.
Usage: uv run python src/roadless/mb_roadless.py [--strict]
Output: data/processed/mb[_strict]/manitoba/
"""
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

from bead import load_bead
from fetch_inputs import RAW, download, fetch_nrn
from nrn_roadless import load_roads as load_nrn
from osm_roadless import CRS
from single_dataset import run

MLI_URL = "https://mli.gov.mb.ca/t20k/shp_zip_files/trn_bas_20k_ln_shp.zip"
NON_ROAD = ("RAIL LINE", "TRAIL", "BRIDGE (PEDESTRIAN", "FOOTPATH")
STRICT_EXTRA = ("CART TRACK", "ACCESSWAY", "ROAD (BACK LANE)", "ROAD - U/C")


def fetch_mli() -> Path:
    shp = RAW / "mb_mli" / "trn_bas_20k_ln.shp"
    if not shp.exists():
        z = download(MLI_URL, RAW / "mb_mli" / "trn_bas_20k_ln_shp.zip")
        with zipfile.ZipFile(z) as f:
            f.extractall(RAW / "mb_mli")
    return shp


def load_roads(nrn: Path, mli: Path, strict: bool = False) -> gpd.GeoDataFrame:
    m = gpd.read_file(mli, engine="pyogrio", columns=["F_TYPE"])
    ft = m["F_TYPE"].fillna("")
    drop = ft.str.startswith(NON_ROAD)
    if strict:
        drop |= ft.str.startswith(STRICT_EXTRA)
    m = m[~drop].to_crs(CRS)
    parts = [load_nrn(nrn)[["geometry"]].assign(source="nrn"),
             m[["geometry"]].assign(source="mli"),
             load_bead("Manitoba").assign(source="bead")]
    return gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs=CRS)


def main(strict: bool) -> None:
    run("mb_strict" if strict else "mb", "Manitoba", "manitoba",
        lambda: load_roads(fetch_nrn("MB"), fetch_mli(), strict), strict=strict)


if __name__ == "__main__":
    main("--strict" in sys.argv)
