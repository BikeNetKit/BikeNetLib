import pytest
import osmnx as ox
import pandas as pd
import geopandas as gpd
from pandas.testing import assert_frame_equal
from bikenetlib.utils import ( # List them in the order appearing in utils.py
    intersects_properly,
    get_principal_bearing,
    filter_seed_points,
)
from shapely.geometry import Point, LineString, MultiLineString


# intersects_properly

@pytest.fixture
def geom_1():
    linestring = LineString([(0, 0), (1, 1), (2, 2)])
    return linestring


@pytest.fixture
def geom_2():
    linestring = LineString([(3, 3), (4, 4), (5, 5)])
    return linestring


def test_intersects_properly(geom_1, geom_2):
    assert intersects_properly(geom_1, geom_2) is False


# filter_seed_points

@pytest.fixture
def seed_point_delta():
    return 500


@pytest.fixture
def snapped_seed_points():
    d = {
        "osmid": ["1", "2", "3"],
        "geometry_generated": [Point(1000, 1000), Point(2000, 2000), Point(3000, 3000)],
    }
    gdf = gpd.GeoDataFrame(d, geometry="geometry_generated", crs="EPSG:3857")
    gdf["geometry_osm"] = gpd.GeoSeries(
        [Point(1001, 1001), Point(10000, 10000), Point(3001, 3001)], crs="EPSG:3857"
    )
    return gdf


@pytest.fixture
def filtered_seed_points():
    d = {"osmid": ["1", "3"], "geometry": [Point(1001, 1001), Point(3001, 3001)]}
    gdf = gpd.GeoDataFrame(d, geometry="geometry", crs="EPSG:3857")
    gdf = gdf.set_index("osmid")
    gdf["osmid"] = gdf.index
    gdf = gdf.iloc[:, [1, 0]]
    return gdf


def test_filter_seed_points(
    snapped_seed_points, filtered_seed_points, seed_point_delta
):
    assert_frame_equal(
        filter_seed_points(snapped_seed_points, seed_point_delta),
        filtered_seed_points,
        check_dtype=False,
    )


# get_principal_bearing

@pytest.fixture
def validation_streets():
    streets_nodes = gpd.read_file(
        "./tests/test_data/oelde_streets.gpkg", layer="nodes"
    ).set_index("osmid")
    streets_edges = gpd.read_file(
        "./tests/test_data/oelde_streets.gpkg", layer="edges"
    ).set_index(["u", "v", "key"])
    streets = ox.convert.graph_from_gdfs(streets_nodes, streets_edges)
    return streets


def test_get_principal_bearing(validation_streets):
    assert get_principal_bearing(validation_streets) == 65.0

