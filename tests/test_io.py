import pytest
from pandas.testing import assert_frame_equal
from networkx.utils.misc import graphs_equal

from tqdm import tqdm
import geopandas as gpd
import osmnx as ox
import os
import shutil

from bikenetlib import constants, io
from bikenetlib.io import (
    export_gdfs,
    slugify,
    import_osm_network,
    initialize_progress_bar,
)

path_test_data = './tests/test_data/'

# export_gdfs
@pytest.fixture
def oelde_gdfs():
    gdfs = {}
    gdfs["Seed points"] = {
        'gdf': gpd.read_file(path_test_data+"oelde_seed_points.geojson"),
        'filename_single': 'oelde_seed_points',
    }
    gdfs["City boundary"] = {
        'gdf': gpd.read_file(path_test_data+"oelde_boundary.geojson"),
        'filename_single': 'oelde_boundary',
    }
    return gdfs

@pytest.fixture
def validation_oelde_gpkg_layer():
    gdf = gpd.read_file(path_test_data+"oelde_export.gpkg", layer="Seed points")
    return gdf

def test_export_gdfs(oelde_gdfs, validation_oelde_gpkg_layer):
    path_test_outputs = './tests/test_outputs/'
    filename = 'oelde_export'

    format = 'gpkg'
    if os.path.exists(path_test_outputs) and os.path.isdir(path_test_outputs):
        shutil.rmtree(path_test_outputs)
    export_gdfs(
        oelde_gdfs, 
        filename=filename, 
        path=path_test_outputs, 
        format=format,
        bar=False,
    )
    assert_frame_equal(
        validation_oelde_gpkg_layer,
        gpd.read_file(path_test_outputs+"oelde_export.gpkg", layer="Seed points"),
        check_dtype=False,
    )
    # Test overwrite
    o = export_gdfs(
        oelde_gdfs, 
        filename=filename, 
        path=path_test_data, # !
        format=format,
        bar=False,
        overwrite=False, # !
    )
    assert o == False

    format = 'geojson'
    if os.path.exists(path_test_outputs) and os.path.isdir(path_test_outputs):
        shutil.rmtree(path_test_outputs)
    export_gdfs(
        oelde_gdfs, 
        filename=filename, 
        path=path_test_outputs, 
        format=format,
        bar=False,
    )
    assert_frame_equal(
        gpd.read_file(path_test_data+"oelde_seed_points.geojson"),
        gpd.read_file(path_test_outputs+"oelde_seed_points.geojson"),
        check_dtype=False,
    )
    assert_frame_equal(
        gpd.read_file(path_test_data+"oelde_boundary.geojson"),
        gpd.read_file(path_test_outputs+"oelde_boundary.geojson"),
        check_dtype=False,
    )
    # Test overwrite
    o = export_gdfs(
        oelde_gdfs, 
        filename=filename, 
        path=path_test_data, # !
        format=format,
        bar=False,
        overwrite=False, # !
    )
    assert o == False

    format = 'shp'
    if os.path.exists(path_test_outputs) and os.path.isdir(path_test_outputs):
        shutil.rmtree(path_test_outputs)
    export_gdfs(
        oelde_gdfs, 
        filename=filename, 
        path=path_test_outputs, 
        format=format,
        bar=False,
    )
    assert_frame_equal(
        gpd.read_file(path_test_data+"oelde_seed_points.geojson"),
        gpd.read_file(path_test_outputs+"oelde_seed_points.shp"),
        check_dtype=False,
    )
    # To do: Some weird FID issue when loading a single-row shape file.
    # shp = gpd.read_file(path_test_outputs+"oelde_boundary.shp")
    # del shp['FID']
    # assert_frame_equal(
    #     gpd.read_file(path_test_data+"oelde_boundary.geojson"),
    #     shp,
    #     check_dtype=False,
    # )

    # Clean up
    if os.path.exists(path_test_outputs) and os.path.isdir(path_test_outputs):
        shutil.rmtree(path_test_outputs)


# slugify
@pytest.fixture
def city_names():
    names = ["Aix-En-Provence", "Alcalá De Henares", "Almería", "Bielsko-Biala", "Chișinău", "Durrës", "L'Hospitalet De Llobregat", "Nîmes", "Umeå", "amsterdam_nl", "áéíóúàèìùòâêîôûäëïöüǎěǐǒǔãẽĩõũăåæçčıłñňøœřßșşšůŷÿźž"]
    return names

@pytest.fixture
def city_names_slugified():
    names = ["aixenprovence", "alcaladehenares", "almeria", "bielskobiala", "chisinau", "durres", "lhospitaletdellobregat", "nimes", "umea", "amsterdam_nl", "aeiouaeiouaeiouaeiouaeiouaeiouaaaccilnnoorssssuyyzz"]
    return names

def test_slugify(city_names, city_names_slugified):
    for n, ns in zip(city_names, city_names_slugified):
        assert slugify(n) == ns


# initialize_progress_bar
@pytest.fixture
def progress_bar_string():
    return "Test string"

def test_initialize_progress_bar(progress_bar_string):
    tqdm_left = initialize_progress_bar(progress_bar_string, total=1, unit="step")
    tqdm_right = tqdm(
        desc=("{:<"+str(constants._PROGRESS_BAR_DESC_LENGTH)+"}").format(progress_bar_string),
        total=1,
        unit="step",
        bar_format='{l_bar}{bar:'+str(constants._PROGRESS_BAR_LENGTH-7)+'}{r_bar}',
        disable=io.silent,
    )
    assert tqdm_left.desc == tqdm_right.desc


# import_osm_network
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

def test_import_osm_network(validation_osm_network):
    g, nodes, edges, boundary_gdf = import_osm_network("osm_network.gpkg", import_path="./tests/test_data/")

    assert graphs_equal(validation_osm_network, g)
