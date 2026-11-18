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
