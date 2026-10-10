"""Utility functions of `bikenetlib`."""

import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import osmnx as ox
from . import osm


def assign_pbi_to_edges(g):
    """Assign a boolean pbi attribute to all edges in a graph depending if they 
    are considered protected bike infrastructure (pbi).

    Parameters
    ----------
    g : networkx.MultiDiGraph
        Simplified graph representing the street network.

    Returns
    -------
    g : networkx.MultiDiGraph
        Simplified graph representing the street network, with added binary edge attribute "pbi".
    """
    for edge in g.edges(keys=True):
        assigned_pbi = 0
        for tag in osm.PBI_DICT:
            if g.edges[edge].get(tag) in osm.PBI_DICT[tag]:
                assigned_pbi = 1
        if not assigned_pbi: # Check if the edge fulfils a subcriterion
            for tag in osm.PBI_DICT_SUB:
                subtag = osm.PBI_DICT_SUB[tag][1].keys()[0]
                if g.edges[edge].get(tag) in osm.PBI_DICT_SUB[tag][0] and g.edges[edge].get(subtag) in osm.PBI_DICT_SUB[tag][1][subtag] and g.edges[edge].get("access") != 'private':
                    assigned_pbi = 1
        g.edges[edge]["pbi"] = assigned_pbi
    return g

    
def nodelist_to_edgetuples(edge_gdf, nodelist):
    """Map a list of ndoes (from `nx.shortest_paths()`) to a list of edge 
    tuples that can be used for indexing an edge geodataframe.

    Useful to apply as a lambda function to turn path nodes into path edges.

    Parameters
    ----------
    edge_gdf : geopandas.geodataframe.GeoDataFrame
        The edges of a spatial network, in a projected CRS.
    nodelist : list
        A list of nodes that make up source and targets of edges.

    Returns
    -------
    edgelist_final : list
        List of edge tuples that can be used for indexing the edge 
        geodataframe.
    """
    edgelist_prelim = zip(nodelist, nodelist[1:])
    edgelist_final = []
    temp_gdf = edge_gdf.sort_index() # To circumvent PerformanceWarning, see https://stackoverflow.com/questions/54307300/what-causes-indexing-past-lexsort-depth-warning-in-pandas
    for edge_prelim in edgelist_prelim:
        if edge_prelim in temp_gdf.index:
            edgelist_final.append(edge_prelim)
        else:
            edgelist_final.append(tuple([edge_prelim[1], edge_prelim[0]]))
    return edgelist_final


def get_principal_bearing(G):
    """Determine the most common (principal) bearing, for the best grid orientation.

    Adapted from: https://github.com/gboeing/osmnx-examples/blob/v0.11/notebooks/17-street-network-orientations.ipynb
    The bearing is determined from edges weighted by length.

    Parameters
    ----------
    G : networkx MultiGraph (undirected)
        The graph from which to determine the principal bearing. Its coordinate reference system must be geographical, not projected.

    Returns
    -------
    principal_bearing: float
        The principal bearing, precise to 5 degrees.
    """

    bearingbins = (
        72  # number of bins to determine bearing. e.g. 72 will create 5 degrees bins
    )

    bearings = {}
    # weight bearings by length (meters)
    city_bearings = []
    for u, v, k, d in G.edges(keys=True, data=True):
        try:
            city_bearings.extend([d["bearing"]] * int(d["length"]))
        except:  # noqa (To do: make specific and remove noqa)
            pass  # Bearings cannot be calculated in rare edge cases.
    b = pd.Series(city_bearings)
    bearings = pd.concat([b, b.map(_reverse_bearing)]).reset_index(drop="True")
    bins = np.arange(bearingbins + 1) * 360 / bearingbins
    count = _count_and_merge(bearingbins, bearings)
    principal_bearing = bins[np.where(count == max(count))][0]

    return principal_bearing


def _reverse_bearing(x):
    """Reverse bearing.

    Adapted from: https://github.com/gboeing/osmnx-examples/blob/v0.11/notebooks/17-street-network-orientations.ipynb

    Parameters
    ----------
    x : float
        The bearing to reverse.

    Returns
    -------
    x_rev : float
        The reversed bearing.
    """
    x_rev = x + 180 if x < 180 else x - 180
    return x_rev


def _count_and_merge(n, bearings):
    """Double, then merge bins to avoid edge effects.

    Make twice as many bins as desired, then merge them in pairs.
    Prevents bin-edge effects around common values like 0° and 90°.
    Adapted from: https://github.com/gboeing/osmnx-examples/blob/v0.11/notebooks/17-street-network-orientations.ipynb

    Parameters
    ----------
    n : int
        Number of bins.
    bearings : pandas.Series
        Series of bearings.

    Returns
    -------
    bearings_merged : numpy.ndarray, dtype=int
        The frequencies of the new merged bearings.
    """
    n *= 2
    bins = np.arange(n + 1) * 360 / n
    count, _ = np.histogram(bearings, bins=bins)

    # move the last bin to the front, so eg 0.01° and 359.99° will be binned together
    count = np.roll(count, 1)
    bearings_merged = count[::2] + count[1::2]
    return bearings_merged


def node_to_edge_attributes(values_nodes, edges):
    """Map node to edge attributes.

    Creates edge attributes by taking the average values of adjacent node attributes.

    Parameters
    ----------
    values_nodes : dict
        Keys: node ids, Values: Node attributes (for example a scalar)
    edges : networkx.classes.reportviews.EdgeView 
        A view of edge attributes of a networkx graph. Could also be a list of tuples of node ids.

    Returns
    -------
    values_edges: dict
        Keys: tuples of node ids, Values: Edge attributes
    """
    values_edges = {}
    for u, v in edges:
        values_edges[(u, v)] = 0.5 * (values_nodes[u] + values_nodes[v])
    return values_edges


def route_nodepairs(nodepairs, edges, g_undir):
    """Route pairs of nodes on the graph `g_undir` to a merged geometry of corresponding OSM nodes and edges.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with node pair integer IDs, columns `source` and `target`.
    edges : geopandas.geodataframe.GeoDataFrame
        The street network, in a projected CRS.
    g_undir : networkx.graph undirected
        Graph to use for routing. The weight variable is "weight".

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with added path nodes and path edges.
    """
    paths = []
    for _, row in df.iterrows():
        paths.append(
            nx.shortest_path(
                G=g_undir,
                source=int(row.source),
                target=int(row.target),
                weight="weight",
            )
        )
    df["path_nodes"] = paths
    df["path_edges"] = df.path_nodes.apply(lambda x: nodelist_to_edgetuples(edges, x))
    return df

