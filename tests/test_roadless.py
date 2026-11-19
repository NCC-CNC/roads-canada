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


def test_bcdra_loader_filters(tmp_path):
    from bcdra_roadless import LAYER, load_roads

    classes = ["resource", "ferry", "driveway", "trail", "local"]
    surfaces = ["rough", "unknown", "paved", "loose", "decommissioned"]
    gdf = gpd.GeoDataFrame(
        {"ID": range(5), "RD_CLASS": classes, "FEAT_TYPE": ["Road"] * 5, "RD_SURFACE": surfaces},
        geometry=[LineString([(0, i * 100), (1000, i * 100)]) for i in range(5)],
        crs=CRS,
    )
    path = tmp_path / "dra.gpkg"
    gdf.to_file(path, layer=LAYER, driver="GPKG")

    # Paper exclusions drop ferry and driveway only; strict also drops trail and decommissioned.
    assert sorted(load_roads(path)["RD_CLASS"]) == ["local", "resource", "trail"]
    assert sorted(load_roads(path, strict=True)["RD_CLASS"]) == ["resource"]


def test_abhfi_loader_filters(tmp_path):
    from abhfi_roadless import LAYER, load_roads

    types = ["ROAD-GRAVEL-1L", "AIRP-RUNWAY", "ROAD-VEGETATED", "ROAD-WINTER", "TRUCK-TRAIL"]
    gdf = gpd.GeoDataFrame(
        {"FEATURE_TY": types, "SOURCE": ["x"] * 5, "YEAR": [2020] * 5},
        geometry=[LineString([(0, i * 100), (1000, i * 100)]) for i in range(5)],
        crs=CRS,
    )
    path = tmp_path / "hfi.gpkg"
    gdf.to_file(path, layer=LAYER, driver="GPKG")

    assert sorted(load_roads(path)["FEATURE_TY"]) == [
        "ROAD-GRAVEL-1L", "ROAD-VEGETATED", "ROAD-WINTER", "TRUCK-TRAIL"]
    assert sorted(load_roads(path, strict=True)["FEATURE_TY"]) == ["ROAD-GRAVEL-1L", "TRUCK-TRAIL"]


def test_ontario_loader_filters(tmp_path):
    from on_roadless import load_roads

    line = lambda y: LineString([(0, y), (1000, y)])  # noqa: E731
    orn = gpd.GeoDataFrame(
        {"OGF_ID": [1, 2, 3], "ROAD_ELEMENT_TYPE": ["ROAD ELEMENT", "FERRY CONNECTION", "VIRTUAL ROAD"]},
        geometry=[line(0), line(100), line(200)], crs="EPSG:4326")
    mnr = gpd.GeoDataFrame(
        {"OGF_ID": [4, 5], "STATUS": ["Open", "Closed"],
         "ROADBED_DESTROYED_IND": ["No", "No"], "ROADBED_PLANTED_IND": ["No", "No"]},
        geometry=[line(300), line(400)], crs="EPSG:4326")
    orn.to_file(tmp_path / "orn.gpkg", layer="roads", driver="GPKG")
    mnr.to_file(tmp_path / "mnr.gpkg", layer="roads", driver="GPKG")

    assert len(load_roads(tmp_path / "orn.gpkg", tmp_path / "mnr.gpkg")) == 4  # ferry out
    assert len(load_roads(tmp_path / "orn.gpkg", tmp_path / "mnr.gpkg", strict=True)) == 2


def test_quebec_loader_filters(tmp_path):
    from qc_roadless import LAYER, load_roads

    gdf = gpd.GeoDataFrame(
        {"IdRte": range(4), "ClsRte": ["Locale", "Rue piétonne", "Liaison maritime", None],
         "CaractRte": [None, None, None, "Chemin privé"], "Gestion": ["FORET"] * 4},
        geometry=[LineString([(0, i * 100), (1000, i * 100)]) for i in range(4)], crs=CRS)
    gdf.to_file(tmp_path / "rqtt.gpkg", layer=LAYER, driver="GPKG")

    assert sorted(load_roads(tmp_path / "rqtt.gpkg")["IdRte"]) == [0, 3]
    assert sorted(load_roads(tmp_path / "rqtt.gpkg", strict=True)["IdRte"]) == [0]


def test_nova_scotia_loader_filters(tmp_path):
    from ns_roadless import load_roads

    descs = ["TRACK", "DRIVEWAY", "TRAIL  - No Vehicular Traffic - No Vehicular Traffic",
             "ROAD - Abandoned - TRACK", "ROAD - Local - 2 Lanes - Paved"]
    gdf = gpd.GeoDataFrame(
        {"feat_code": ["a"] * 5, "feat_desc": descs},
        geometry=[LineString([(0, i * 100), (1000, i * 100)]) for i in range(5)], crs=CRS)
    gdf.to_file(tmp_path / "ns.gpkg", layer="roads", driver="GPKG")

    assert sorted(load_roads(tmp_path / "ns.gpkg")["feat_desc"]) == [
        "ROAD - Abandoned - TRACK", "ROAD - Local - 2 Lanes - Paved", "TRACK"]
    assert sorted(load_roads(tmp_path / "ns.gpkg", strict=True)["feat_desc"]) == [
        "ROAD - Local - 2 Lanes - Paved", "TRACK"]


def test_yukon_loader_filters(tmp_path):
    from yt_roadless import load_roads

    line = lambda y: LineString([(0, y), (1000, y)])  # noqa: E731
    net = gpd.GeoDataFrame({"ROAD_TYPE": ["Local / Street", "Winter", "Driveway"]},
                           geometry=[line(0), line(100), line(200)], crs="EPSG:4326")
    forest = gpd.GeoDataFrame({"ROAD_CLASS": ["Primary Road", "Trail"]},
                              geometry=[line(300), line(400)], crs="EPSG:4326")
    net.to_file(tmp_path / "n.gpkg", layer="roads", driver="GPKG")
    forest.to_file(tmp_path / "f.gpkg", layer="roads", driver="GPKG")

    assert len(load_roads(tmp_path / "n.gpkg", tmp_path / "f.gpkg")) == 5
    assert len(load_roads(tmp_path / "n.gpkg", tmp_path / "f.gpkg", strict=True)) == 2
