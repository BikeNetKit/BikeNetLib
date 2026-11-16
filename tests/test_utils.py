import pytest
from pandas.testing import assert_frame_equal

import osmnx as ox
import geopandas as gpd
from shapely.geometry import LineString, Point

from bikenetlib.utils import (
    add_point_data_to_net,
    get_principal_bearing,
)


# get_principal_bearing
@pytest.fixture
def validation_osm_network():
    """Acquire:
    >>> g=ox.graph_from_point((55.658328, 12.589548), 250)
    >>> ox.io.save_graph_geopackage(g, "osm_network.gpkg")
    """
    osm_network_nodes = gpd.read_file(
        "./tests/test_data/osm_network.gpkg", layer="nodes"
    ).set_index("osmid")
    osm_network_edges = gpd.read_file(
        "./tests/test_data/osm_network.gpkg", layer="edges"
    ).set_index(["u", "v", "key"])
    osm_network = ox.convert.graph_from_gdfs(osm_network_nodes, osm_network_edges)
    return osm_network

def test_get_principal_bearing(validation_osm_network):
    assert get_principal_bearing(validation_osm_network) == 10.0

    # Now drop bearings. They should be re-added by the function.
    for _, _, d in validation_osm_network.edges(data=True):
        if 'bearing' in d:
            del d["bearing"]
    assert get_principal_bearing(validation_osm_network) == 10.0



# add_point_data_to_net
@pytest.fixture
def routed_edges_crashes():
    # Nodes of the graph
    A = (800,1800)
    B = (1300,2000)
    C = (1800,1800)
    D = (900,1400)
    E = (1300,1300)
    F = (1800,1200)
    G = (800,800)
    H = (1300,800)

    # Auxiliary nodes
    Z = (1150,1100)

    g = {
        'geometry': [
            LineString([A,B]),
            LineString([A,D]),
            LineString([B,C]),
            LineString([B,E]),
            LineString([C,F]),
            LineString([D,E]),
            LineString([D,G]),
            LineString([E,F]),
            LineString([E,Z,H]),
            LineString([F,H]),
            LineString([G,H])
        ]
    }
    graph = gpd.GeoDataFrame(g, geometry="geometry", crs = "EPSG:3857")
    return graph

@pytest.fixture
def crashes_data():
    # Points from crashes data          In ESPG:3857
    I = Point(0.0089832,0.0080848)      # (1000,900)
    J = Point(0.0125764,0.014373)       # (1400,1600)
    K = Point(0.0080848,0.0134747)      # (900,1500)
    L = Point(0.0071865,0.0116781)      # (800,1300)
    M = Point(0.0062882,0.0134747)      # (700,1500)
    N = Point(0.0098815,0.0134747)      # (1100,1500)
    O = Point(0.0161697,0.0026949)      # (1800,300)
    P = Point(0.014373,0.0116781)       # (1600,1300)
    Q = Point(0.0071865,0.0089832)      # (800,1000)
    R = Point(0.0098815,0.0098815)      # (1100,1100)
    S = Point(0.014373,0.0215596)       # (1600,2400)
    T = Point(0.017068,0.0152714)       # (1900,1700)
    U = Point(0.0107798,0.0062882)      # (1200,700)
    V = Point(0.0089832,0.0161697)      # (1000,1800)
    W = Point(0.0161697,0.0098815)      # (1800,1100)

    c = {
        'geometry': [I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W],
        'num': [1,1,2,3,1,1,1,3,5,1,1,1,1,2,1]
    }
    crashes = gpd.GeoDataFrame(c, geometry="geometry", crs = "EPSG:4326")
    return crashes

@pytest.fixture
def routed_edges_with_crashes_data():
    # Nodes of the graph
    A = (800,1800)
    B = (1300,2000)
    C = (1800,1800)
    D = (900,1400)
    E = (1300,1300)
    F = (1800,1200)
    G = (800,800)
    H = (1300,800)

    # Auxiliary nodes
    Z = (1150,1100)

    g = {
        'num_points': [
            2,  #[A,B]
            3,  #[A,D]
            1,  #[B,C]
            1,  #[B,E]
            1,  #[C,F]
            1,  #[D,E]
            8,  #[D,G]
            3,  #[E,F]
            1,  #[E,Z,H]
            1,  #[F,H]
            2,  #[G,H]
        ],
        'geometry': [
            LineString([A,B]),
            LineString([A,D]),
            LineString([B,C]),
            LineString([B,E]),
            LineString([C,F]),
            LineString([D,E]),
            LineString([D,G]),
            LineString([E,F]),
            LineString([E,Z,H]),
            LineString([F,H]),
            LineString([G,H]),
        ]
    }
    graph = gpd.GeoDataFrame(g, geometry="geometry", crs = "EPSG:3857")
    return graph

def test_add_point_data_to_net_case_success_simple(routed_edges_crashes, crashes_data, routed_edges_with_crashes_data):
    # constants._CRS_CALCULATIONS = '3857'
    assert_frame_equal(
        add_point_data_to_net(crashes_data, routed_edges_crashes),
        routed_edges_with_crashes_data,
        check_dtype=False
    )


@pytest.fixture
def turin_routed_edges_crashes():
    g = gpd.read_file("./tests/test_data/turin_edges_gdf.gpkg")
    return g

@pytest.fixture
def turin_accidents_data():
    c = gpd.read_file("./tests/test_data/turin_crashes.gpkg")
    return c

@pytest.fixture
def turin_routed_edges_with_crashes_data():
    g = gpd.read_file("./tests/test_data/turin_edges_gdf_with_crashes.gpkg")
    return g

def test_add_point_data_to_net_case_success_turin(turin_accidents_data, turin_routed_edges_crashes, turin_routed_edges_with_crashes_data):
    # constants._CRS_CALCULATIONS = '3857'
    result = add_point_data_to_net(turin_accidents_data, turin_routed_edges_crashes)

    diff_mask = result['num_points'] != turin_routed_edges_with_crashes_data['num_points']
    if diff_mask.any():
        print("\n\nDifferences found:")
        print(result.loc[diff_mask, ['num_points']])
        print("\nExpected:")
        print(turin_routed_edges_with_crashes_data.loc[diff_mask, ['num_points']])
    
    assert_frame_equal(
        add_point_data_to_net(turin_accidents_data, turin_routed_edges_crashes),
        turin_routed_edges_with_crashes_data,
        check_dtype=False
    )
