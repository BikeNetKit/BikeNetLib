"""Import/Output functions of `bikenetlib`, including format conversions and 
user feedback tools.

silent : bool, default False
    If set to True, suppresses all user feedback. Useful for batch exports.
"""

silent = False

import os
import re
from tqdm import tqdm
from . import constants, osm, _overpass
import geopandas as gpd
import osmnx as ox


def export_gdfs(
        gdfs,
        filename='exported_data',
        path="./",
        format='gpkg',
        overwrite=True,
        crs='4326',
        bar=False
    ):
    """Export GeoDataFrames as geojson, gpkg, or shp file(s).

    If crs=='4326' and format=='geojson', export with RFC7946.

    Parameters
    ----------
    gdfs : dict
        Dictionary with the layer names as keys with dict values that contain 
        gdf and single filename. Structure:
        {
            'layername1': {'gdf': gdf1, 'filename_single':str},
            'layername2': {'gdf': gdf2, 'filename_single':str},
            ...
        }
        `filename_single` is relevant for geojson and shp files which ignore
        `filename` and export each gdf as individual files. `layername` is 
        relevant for gpkg which exports all gdfs merged into one file 
        `filename` as their own layers.
    filename : str, default 'exported_data'
        Name of exported file, if exported as gpkg.
    path : str, default './'
        Export path.
    format : {'gpkg', 'geojson', 'shp'}, default 'gpkg'
        Export file format.
    overwrite : bool, default True
        Decision whether to overwrite existing files.
    crs : str, default '4326'
        Coordinate Reference System of exported data.
    bar : bool, default False
        Decision whether to show a progress bar.

    Returns
    -------
    bool
        Returns True if all files have been written. If overwrite is set to 
        False and at least one file already existed, returns False. 
    """
    os.makedirs(path, exist_ok=True)

    format_driver = {'gpkg': "GPKG", 'geojson': "GeoJSON", 'shp': "ESRI Shapefile"}
    d = format_driver[format]
    
    if bar: progress_bar = initialize_progress_bar("Exporting data", len(gdfs), "file")

    if format == 'gpkg': # Export as one file with layers
        f = path+filename+'.'+format
        # Check if file exists, and remove if overwrite
        if os.path.exists(f):
            if not overwrite:
                return False
            else:
                os.remove(f)
        # Export one gpkg with layers
        for layername, gdfinfo in gdfs.items():
            gdfinfo['gdf'].to_file(f, driver=d, layer=layername)
            if bar: progress_bar.update(1)

    elif format == 'geojson' or format == 'shp': # Export as individual files
        # Check if files exists, and remove if overwrite
        for gdfinfo in gdfs.values():
            f = path+gdfinfo['filename_single']+'.'+format
            if os.path.exists(f):
                if not overwrite:
                    return False
                else:
                    os.remove(f)
        # Export individual files
        for layername, gdfinfo in gdfs.items():
            f = path+gdfinfo['filename_single']+'.'+format
            if format == 'geojson' and crs == '4326':
                gdfinfo['gdf'].to_file(f, driver=d, RFC7946="YES")
            else:
                gdfinfo['gdf'].to_file(f, driver=d)
            if bar: progress_bar.update(1)

    if bar: progress_bar.close()
    return True


def import_osm_network(osm_network, import_path='./', make_undirected=False, project_crs=False):
    """Import an OSM transport network from gpkg file as networkx graph and 
    GeoDataframes of nodes and edges, with a boundary around the nodes.

    Parameters
    ----------
    osm_network : str
        The OSM transport network is loaded from this file. Must be a gpkg file 
        in unprojected CRS EPSG:4326 with layers nodes and edges, with the 
        structure that a OSMnx transport network ``g`` has. This must be a 
        MultiGraph. The nodes layer must have an `osmid` field. The edges layer
        must have the fields `u`, `v`, and `key`. For example:

        >>> g = ox.graph_from_place("Barcelona", network_type='drive')
        >>> ox.io.save_graph_geopackage(g, "Barcelona_streets.gpkg")
    import_path : str, default './'
        Path to import files.
    make_undirected : bool, default False
        Whether to make the network undirected. This will drop the OSMnx `key`
        field.
    project_crs : bool | str, default False
        If bool and False, do not project. If str, project the nodes and edges with the given `project_crs` EPSG string. The output graph `g` is never 
        projected.

    Returns
    -------
    g : networkx.classes.multigraph.MultiGraph
        Extracted networkX graph. Unprojected.
    nodes : geopandas.geodataframe.GeoDataFrame
        Extracted OSM nodes. Unprojected if project_crs is False, otherwise
        projected via project_crs.
    edges : geopandas.geodataframe.GeoDataFrame
        Extracted OSM edges. Unprojected if project_crs is False, otherwise
        projected via project_crs.    
    boundary_gdf : geopandas.geodataframe.GeoDataFrame
        Convex hull of the network nodes. Unprojected if project_crs is False,
        otherwise projected via project_crs. 
    """
    nodes = gpd.read_file(import_path+osm_network, layer='nodes')
    edges = gpd.read_file(import_path+osm_network, layer='edges')

    # Set indices as required by osmnx.convert.graph_from_gdfs
    # See: https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.utils_graph.graph_from_gdfs
    nodes = nodes.set_index(['osmid'])
    edges = edges.set_index(['u', 'v', 'key'])

    g = ox.convert.graph_from_gdfs(nodes, edges)

    if make_undirected:
        g = g.to_undirected() # make undirected (dropping OSMnx key fields!)

    if project_crs is not False:
        edges = edges.to_crs(project_crs)
        nodes = nodes.to_crs(project_crs)

    boundary_gdf = gpd.GeoDataFrame(gpd.GeoSeries(nodes.union_all().convex_hull), geometry=0, crs=nodes.crs) 
    # To do: Add a buffering option (calculations via degrees due to being unprojected)
    return g, nodes, edges, boundary_gdf


def slugify(s): 
    """Slugify a string.
    
    Adapted from: https://github.com/Chalarangelo/30-seconds-of-code/blob/master/content/snippets/python/s/slugify.md

    Parameters
    ----------
    s : str
        String to slufigy.

    Returns
    -------
    s : str
        Slugified string.

    Notes
    -----
    A clean global solution would be using unidecode, but we do not want
    extra dependencies for this. We assume European city names in latin
    alphabet, and some special letters like Hungarian ő already mapped.
    """
    s = s.lower().strip()
    s = re.sub(r'[\s-]+', '', s) # Remove white spaces, -
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'^-+|-+$', '', s)
    tab = str.maketrans(
        "áéíóúàèìùòâêîôûäëïöüǎěǐǒǔãẽĩõũăåæçčıłñňøœřßșşšůŷÿźž",
        "aeiouaeiouaeiouaeiouaeiouaeiouaaaccilnnoorssssuyyzz"
    )
    s = s.translate(tab)
    return s


def initialize_progress_bar(desc_string, total=1, unit="step"):
    """Initialize tqdm progress bar.
    """
    return tqdm(
        desc=("{:<"+str(constants._PROGRESS_BAR_DESC_LENGTH)+"}").format(desc_string),
        total=total,
        unit=unit,
        bar_format='{l_bar}{bar:'+str(constants._PROGRESS_BAR_LENGTH-7)+'}{r_bar}',
        disable=silent,
    )
