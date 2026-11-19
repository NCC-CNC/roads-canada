"""Roadless-area metrics for the Northwest Territories: NRN plus BEAD roads.

The paper's merged baseline for NT was the NRN plus BEAD 2010 and 2015 roads
(note 13). NRN keeps Winter roads (note 10). See `bead.py` for the BEAD source
and its caveats.
Usage: uv run python src/roadless/nt_roadless.py
Output: data/processed/nt/northwest-territories/
"""
import geopandas as gpd
import pandas as pd

from bead import load_bead
from fetch_inputs import fetch_nrn
from nrn_roadless import load_roads as load_nrn
from osm_roadless import CRS
from single_dataset import run


def main() -> None:
    def load():
        parts = [load_nrn(fetch_nrn("NT"))[["geometry"]].assign(source="nrn"),
                 load_bead("Northwest Territories").assign(source="bead")]
        return gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs=CRS)
    run("nt", "Northwest Territories", "northwest-territories", load)


if __name__ == "__main__":
    main()
