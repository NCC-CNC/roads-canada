"""Synthetic check of the roadless-area calculation with a known answer."""
import sys
from pathlib import Path

import geopandas as gpd
from shapely.geometry import LineString, box

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "roadless"))

from osm_roadless import BUFFER_M, CRS, roadless_patches, summarize  # noqa: E402


def test_single_road_across_square():
    # 10 km square of land with one road along the middle of the west-east axis.
    # A 1 km buffer on each side removes a 2 km wide strip, leaving two
    # 10 km x 4 km patches: 80 km2 roadless out of 100 km2.
    side = 10_000
    land = gpd.GeoDataFrame(geometry=[box(0, 0, side, side)], crs=CRS)
    road = gpd.GeoDataFrame(geometry=[LineString([(0, side / 2), (side, side / 2)])], crs=CRS)

    patches = roadless_patches(road, land)
    stats = summarize(patches, land.geometry.area.sum() / 1e6)

    assert BUFFER_M == 1000
    assert len(patches) == 2
    assert abs(stats["roadless_km2"] - 80.0) < 1e-6
    assert abs(stats["pct_roadless"] - 80.0) < 1e-6
    assert abs(stats["max_km2"] - 40.0) < 1e-6


def test_no_roads_leaves_all_land():
    land = gpd.GeoDataFrame(geometry=[box(0, 0, 5_000, 5_000)], crs=CRS)
    roads = gpd.GeoDataFrame(geometry=[], crs=CRS)
    patches = roadless_patches(roads, land)
    assert len(patches) == 1
    assert abs(patches["area_km2"].sum() - 25.0) < 1e-6


def test_verify_zip_rejects_truncated(tmp_path):
    import pytest
    from run_regions import verify_zip

    good = tmp_path / "good.zip"
    import zipfile
    with zipfile.ZipFile(good, "w") as z:
        z.writestr("a.txt", "x" * 1000)
    verify_zip(good)
    bad = tmp_path / "bad.zip"
    bad.write_bytes(good.read_bytes()[:-30])
    with pytest.raises(Exception):
        verify_zip(bad)


def test_nrn_loader_filters_road_class(tmp_path):
    from nrn_roadless import load_roads

    gdf = gpd.GeoDataFrame(
        {
            "NID": ["a", "b"], "ROADCLASS": ["Collector", "Winter"],
            "PAVSTATUS": ["Paved", "Unknown"], "CLOSING": ["Unknown", "Unknown"],
            "REVDATE": ["20200101", "20200101"],
        },
        geometry=[LineString([(0, 0), (1000, 0)]), LineString([(0, 500), (1000, 500)])],
        crs=CRS,
    )
    path = tmp_path / "nrn.gpkg"
    gdf.to_file(path, layer="NRN_XX_1_0_ROADSEG", driver="GPKG")

    assert len(load_roads(path)) == 2  # default keeps every class, as the paper did
    assert list(load_roads(path, excluded=["Winter"])["ROADCLASS"]) == ["Collector"]
