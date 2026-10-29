import pytest
import osmnx as ox
import geopandas as gpd
from pandas.testing import assert_frame_equal
from bikenetlib.utils import ( # List them in the order appearing in utils.py
    get_principal_bearing,
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

    # Now drop bearings. They should be re-added by the function.
    for _, _, d in validation_streets.edges(data=True):
        if 'bearing' in d:
            del d["bearing"]
    assert get_principal_bearing(validation_streets) == 65.0

