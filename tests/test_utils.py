import pytest
from pandas.testing import assert_frame_equal

import osmnx as ox
import geopandas as gpd

from bikenetlib.utils import (
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
