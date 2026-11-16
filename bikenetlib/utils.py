"""Utility functions of `bikenetlib`."""

import numpy as np
np.set_printoptions(legacy='1.25') # Do not report a float as "np.float64(..)"
import pandas as pd
import geopandas as gpd
import networkx as nx
import osmnx as ox
from pyproj import Transformer
import shapely
from shapely.strtree import STRtree
from . import constants, osm, _overpass


def add_point_data_to_net(points, edges, matching_distance=500):
    """Match point data to network edges.

    Parameters
    ----------
    points : geopandas.geodataframe.GeoDataFrame
        A geodataframe of unprojected point geometries, optional having a 
        column ``num`` containing an integer. This could be (number of) point 
        events like crashes or citizen feedback to improve bike infrastructure. 
        If a ``num`` column is not provided, assumes 1 per point.
    edges : geopandas.geodataframe.GeoDataFrame
        A geodataframe of projected spatial network edges. This is the routed 
        network of seed points. It has to be in a distance-preserving projected
        CRS, so '3857' (WGS 84 / Pseudo-Mercator) would be wrong!
    matching_distance : int, default 500
        Matching distance in meters.

    Returns
    -------
    edges_with_data : geopandas.geodataframe.GeoDataFrame
        The same spatial network edges, but with a new int column 
        ``num_points`` populated with the summed up ``num`` values of all 
        points, matched to the closest links if within `matching_distance`. 
    """
    edges_with_data = edges.copy()
    points_projected = points.to_crs(edges_with_data.crs)

    # If column "num" is not provided assume 1 event per point
    if 'num' in points_projected.columns:
        nums = points_projected['num']
    else:
        nums = [1] * len(points_projected)

    # Initialize the 'num_points' column to 0 for all edges
    edges_with_data['num_points'] = 0 * len(edges_with_data)

    # Get geometries of edges and points
    edges_geoms = edges_with_data['geometry']
    points_geoms = points_projected['geometry']

    # Build an r-tree spatial index by position for subsequent iloc
    rtree = STRtree(edges_geoms)    
                            
    for point in points_geoms.items(): # point = (id, POINT(x, y))
        # Query the tree for all the edges within the matching distance of the point
        edges_within_matching_distance = rtree.query(
            point[1],
            predicate='dwithin',
            distance=matching_distance
        )

        # If no edges are within the matching distance, continue to the next point
        if len(edges_within_matching_distance) == 0:
            continue

        # Calculate the distances from the point to each of the edges, and round to 10 decimal places to avoid floating point precision issues
        distances = []
        for edge in edges_within_matching_distance:
            distance = np.around(shapely.distance(point[1], edges_geoms.iloc[edge]), decimals=10)
            distances.append(distance)

        # Get the edges that are closest to the point
        closest_edges = edges_within_matching_distance[np.where(distances == np.min(distances))]

        # Get the lowest index of the closest edges
        closest_edges_min_index = np.sort(closest_edges)[0]

        # Get the number of events at the point
        num = nums[point[0]]

        # Add the number of events to the nearest edge
        edges_with_data.loc[closest_edges_min_index, 'num_points'] += num

    # Move the 'geometry' column to the end of the GeoDataFrame
    # Necessary for testing the function
    cols = [c for c in edges_with_data.columns if c != 'geometry'] + ['geometry']
    edges_with_data = edges_with_data[cols]

    return edges_with_data


def add_trip_data_to_net(trips, A, matching_distance=500):
    """Match trip data to network edges.

    First, match origin and destination points given in trips to the nodes.
    Only consider trips where both origins and nodes are matched within
    `matching_distance`. Then, for each trip, find the shortest path over the
    edges from matched origin node to matched destination node, and add 1 (or
    optionally ``num`` if column provided in trips) to the affected edges.

    Parameters
    ----------
    trips : pandas DataFrame
        A dataframe of unprojected origin-destination coordinates (columns: 
        ``o_lat, o_lon, d_lat, d_lon``), with each row encoding a trip, in 
        unprojected CRS EPSG:4326. Optional with a column ``num`` containing an 
        integer. This could be (number of) trip events. If ``num`` column is 
        not provided, assumes 1 per trip.
    A : networkx.graph
        Spatial network, for example a street network. Needs to have a graph
        `crs` attribute. Set as such: `A.graph['crs'] = '1234'`. It has to be 
        a distance-preserving projected CRS, so '3857' (WGS 84 / 
        Pseudo-Mercator) would be wrong!
    matching_distance : int, default 500
        Matching distance in meters.

    Returns
    -------
    graph_with_data : networkx.graph
        The same graph created from triangulation edges list, but with a new
        edge attribute 'num_trips' populated with the summed up ``num`` values 
        of all trips where both origins and destinations could be matched to 
        the closest network nodes within `matching_distance`. 
    """
    graph_with_data = A.copy()
    transformer = Transformer.from_crs("EPSG:4326", graph_with_data.graph['crs'], always_xy=True)

    # If column "num" is not provided assume 1 trip per origin-destination (OD) pair
    if 'num' in trips.columns:
        nums = trips['num']
    else:
        nums = [1] * len(trips)

    # Project trip data
    trips_projected = trips.copy()
    trips_projected['o_lon'], trips_projected['o_lat'] = transformer.transform(trips['o_lon'], trips['o_lat'])
    trips_projected['d_lon'], trips_projected['d_lat'] = transformer.transform(trips['d_lon'], trips['d_lat'])

    # Match given origins and destinations to the closest nodes in the network
    o_nodes, o_distances = ox.distance.nearest_nodes(graph_with_data, trips_projected['o_lon'], trips_projected['o_lat'], return_dist=True)
    d_nodes, d_distances = ox.distance.nearest_nodes(graph_with_data, trips_projected['d_lon'], trips_projected['d_lat'], return_dist=True)

    # Add number of trips to graph
    trip_dict = dict(zip(graph_with_data.edges, [0] * len(graph_with_data.edges)))

    for o_node, o_distance, d_node, d_distance, num in zip(o_nodes, o_distances, d_nodes, d_distances, nums):
        # If:
        #   - origin and destination are snapped to the same node, or
        #   - origin is >500m away from the snapped node, or
        #   - destination is >500m away from the snapped node
        # no trips are added
        if o_node == d_node or o_distance > matching_distance or d_distance > matching_distance:
            continue  

        # Get shortest path between the snapped orgin and destination nodes
        path = nx.shortest_path(graph_with_data, source=o_node, target=d_node, weight="distance")
        path_edges = list(zip(path[:-1], path[1:]))

        # Add the number of trips to each edge of the shortest path
        for i, edge_id in enumerate(path_edges):
            if edge_id in trip_dict:
                trip_dict[edge_id] += num
            else:
                edge_id = (path[i + 1], path[i])  # Inverse node order
                if edge_id in trip_dict:
                    trip_dict[edge_id] += num

    nx.set_edge_attributes(graph_with_data, trip_dict, "num_trips")
    return graph_with_data


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
        if not assigned_pbi: # Check if the edge fulfills a subcriterion
            for tag in osm.PBI_DICT_SUB:
                subtag = list(osm.PBI_DICT_SUB[tag][1].keys())[0]
                if g.edges[edge].get(tag) in osm.PBI_DICT_SUB[tag][0] and g.edges[edge].get(subtag) in osm.PBI_DICT_SUB[tag][1][subtag] and g.edges[edge].get("access") != 'private':
                    assigned_pbi = 1
        g.edges[edge]["pbi"] = assigned_pbi
    return g

    
def nodelist_to_edgetuples(edge_gdf, nodelist):
    """Map a list of nodes (from `nx.shortest_paths()`) to a list of edge 
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


def get_principal_bearing(G, bearingbins = 72):
    """Determine the most common (principal) bearing, for the best grid orientation.

    Adapted from: https://github.com/gboeing/osmnx-examples/blob/v0.11/notebooks/17-street-network-orientations.ipynb
    The bearing is determined from edges weighted by length.

    Parameters
    ----------
    G : networkx MultiGraph (undirected)
        The graph from which to determine the principal bearing. Its coordinate reference system must be geographical, not projected.
    bearing_bins : int, default 72
        Number of bins to determine bearing. e.g. 72 will create 5 degrees 
        bins.

    Returns
    -------
    principal_bearing: float
        The principal bearing, precise to 5 degrees.
    """

    # Check if bearing has already been added
    edge_attributes = list(list(G.edges(data=True))[0][-1].keys())
    if "bearing" not in edge_attributes:
        G = ox.add_edge_bearings(G)

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


def route_nodepairs(nodepairs, edges, g_undir, weight="weight"):
    """Route pairs of nodes on the graph `g_undir` to a merged geometry of corresponding OSM nodes and edges.

    Parameters
    ----------
    nodepairs : pandas.DataFrame
        Dataframe with node pair integer IDs, columns `source` and `target`.
    edges : geopandas.geodataframe.GeoDataFrame
        The street network, in a projected CRS.
    g_undir : networkx.graph undirected
        Graph to use for routing. 
    weight : string, default "weight"
        The name of the weight variable.

    Returns
    -------
    nodepairs : pandas.DataFrame
        Dataframe of node pairs with added path nodes and path edges.
    """
    paths = []
    for _, row in nodepairs.iterrows():
        paths.append(
            nx.shortest_path(
                G=g_undir,
                source=int(row.source),
                target=int(row.target),
                weight=weight,
            )
        )
    nodepairs["path_nodes"] = paths
    nodepairs["path_edges"] = nodepairs.path_nodes.apply(lambda x: nodelist_to_edgetuples(edges, x))
    return nodepairs


def weight_distances(B, num_types, import_data_impact=9, inverted=False):
    """Get weighted distances by edge attribute `num_types`.

    Parameters
    ----------
    B : networkx.classes.multigraph.MultiGraph
        The routed, grown bicycle network graph, where edges have the attribute 
        `num_types`. The numerical attribute 'distance' must exist for all 
        edges.
    num_types : str
        Name of the attribute to weight the distances.
    import_data_impact : float, default 9
        Impact of `num_types` data on results. Must be non-negative.
    inverted : bool, default False
        Whether to invert the weighting (multiply instead of divide).

    Returns
    -------
    dist_weighted_by_types_dict : dict
        Dictionary where keys are the edges (tuples of node ids), and values 
        are the weighted distances following [1]_.

    Notes
    -----
    The calculation follows [1]_, only without +1 in the numerator and with a 
    small epsilon to prevent division by zero.

    References
    ----------
    .. [1] P. Folco, L. Gauvin, M. Tizzoni, M. Szell, `Data-driven micromobility network planning for demand and safety`, Environment and planning B: Urban analytics and city science 50(8), 2087-2102 (2023)
    """
    num_types_dict = nx.get_edge_attributes(B, num_types)
    dist_dict = nx.get_edge_attributes(B, 'distance')

    num_types_per_km_dict = {}
    for k,d in dist_dict.items():
        if d != 0:
            num_types_per_km_dict[k] = 1000*num_types_dict[k]/d
        else: # To do: How can it be zero? Turin self-loop: (1668523317, 1668523317)
            num_types_per_km_dict[k] = 0
    max_n = max(num_types_per_km_dict.values())+1e-10

    dist_weighted_by_types_dict = {}
    for k,d in dist_dict.items():
        if inverted:
            dist_weighted_by_types_dict[k] = d * (1+import_data_impact*(num_types_per_km_dict[k]/max_n))
        else:
            dist_weighted_by_types_dict[k] = d / (1+import_data_impact*(num_types_per_km_dict[k]/max_n))

    return dist_weighted_by_types_dict
