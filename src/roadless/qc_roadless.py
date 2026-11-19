"""Roadless-area metrics for Quebec from the Referentiel quebecois du transport terrestre (RQTT).

Successor to AQreseau+, which the paper used. Layer `Reseau_routier`
(1,475,428 segments, 656,523 km in the 2026-11 edition). Licence CC-BY 4.0
(MRNF, attribution required). Download: `fetch_inputs.py rqtt`.

Filter on `ClsRte`, default = the paper's exclusion (Rue pietonne) plus
Liaison maritime (ferry links, excluded for other provinces). `--strict` also
drops `CaractRte` Chemin prive and Saisonnier, as an upper bound on roadless
area. Forest road classes (`Cls_CheFor`) stay in; their coding is not used.
Usage: uv run python src/roadless/qc_roadless.py [--strict]
Output: data/processed/qc[_strict]/quebec/
"""
import sys
from pathlib import Path

import geopandas as gpd

from fetch_inputs import fetch_rqtt
from osm_roadless import CRS
from single_dataset import run

LAYER = "Reseau_routier"
EXCLUDED_CLASS = ["Rue piétonne", "Liaison maritime"]
STRICT_EXTRA_CARACT = ["Chemin privé", "Saisonnier"]


def load_roads(gpkg: Path, strict: bool = False) -> gpd.GeoDataFrame:
    roads = gpd.read_file(gpkg, layer=LAYER, engine="pyogrio",
                          columns=["IdRte", "ClsRte", "CaractRte", "Gestion"])
    keep = ~roads["ClsRte"].isin(EXCLUDED_CLASS)
    if strict:
        keep &= ~roads["CaractRte"].isin(STRICT_EXTRA_CARACT)
    return roads[keep].to_crs(CRS)


def main(strict: bool) -> None:
    run("qc_strict" if strict else "qc", "Quebec", "quebec",
        lambda: load_roads(fetch_rqtt(), strict), strict=strict)


if __name__ == "__main__":
    main("--strict" in sys.argv)
