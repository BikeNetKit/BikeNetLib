import geopandas as gpd
import osmnx as ox

def prepare_network(city_name, proj_crs, network_type='all_public', custom_filter=None, retain_all=True, city_boundary_file=None):
    """Download and prepare a street network from OSM via OSMnx

    Downloads a network with a given network_type and custom_filter using ox.graph_from_place.
    Then, stores the undirected OSM data in gdfs and projects using proj_crs.

    Parameters
    ----------
    city_name : str
        Name of the city that the analysis should be performed on. Overruled (for data fetching) if city_boundary_file is set.
    proj_crs : str
        Coordinate reference system that is used to project osm data.
    network_type : {“all”, “all_public”, “bike”, “drive”, “drive_service”, “walk”} 
        What type of street network to retrieve if custom_filter is None.
    custom_filter : (str | list[str] | None)
        A custom ways filter to be used instead of the network_type presets
    retain_all : bool, default True
        If True, return the entire graph even if it is not connected, useful for disconnected bicycle networks. If False, retain only the largest weakly connected component, useful for road networks.
    city_boundary_file : (str | None), default None
        If not set to None, the study area will be selected from the (Multi)Polygon provided in the city_boundary_file shape file. For example, "copenhagen.shp".

    Returns
    -------
    nodes : geopandas.geodataframe.GeoDataFrame
        Extracted OSM nodes, projected
    edges : geopandas.geodataframe.GeoDataFrame
        Extracted OSM edges, projected
    g_undir : networkx.classes.multigraph.MultiGraph
        Extracted networkX graph, undirected
    """

    # Fetch street network data from osmnx
    if city_boundary_file is None:
        g = ox.graph_from_place(
        city_name, network_type=network_type, custom_filter=custom_filter, retain_all=retain_all
        )
    else:
        shp = gpd.read_file(city_boundary_file)
        city_boundary_polygon = shp.iloc[0].geometry
        g = ox.graph_from_polygon(
        city_boundary_polygon, network_type=network_type, custom_filter=custom_filter, retain_all=retain_all
        )

    g_undir = g.to_undirected().copy() # convert to undirected (dropping OSMnx keys!)

    # Export osmnx data to gdfs
    nodes, edges = nx_to_nodes_edges(g_undir, proj_crs)
    return nodes, edges, g_undir

def download_pois(): # To develop
    pass

def save_to_file(): # To develop
    pass