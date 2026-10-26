# CONSTANTS
General constants.

## Single-use
- X gbn: `_BEARING_BINS`: Make `get_principal_bearing()` default parameter.

## Multi-use
- X `_PROGRESS_BAR_DESC_LENGTH`: required for `io.initialize_progress_bar()`
- X `_PROGRESS_BAR_LENGTH`: required for `io.initialize_progress_bar()`
- `_ROUTING_PENALTY`: required for `utility.weigh_edges()`


# IO
Input/Output like downloads, imports, exports, but also format conversions and user feedback tools.

## Multi-use
- X `slugify()`
- X `initialize_progress_bar()`: require tqdm
- X `export_gdfs()`
- `import_network()`, `prepare_nodes_edges()`: align gbn-fbn
- `download_network()`: align gbn-fbn
- `_resolve_crs_calculations()`
- `_print_header()`, `_print_footer()`: align gbn-rest, later

## Single-use
- gbn: `nx_to_nodes_edges()`, `prepare_nodes_edges()`: explore how to turn general-purpose
- gbn: `df_from_graph()`: explore how to turn general-purpose


# OSM
OSM constants.

## Multi-use
- X import custom tags
- X `GROWABLE_NETWORK_CUSTOM_FILTER` -> `CARPBI_NETWORK_CUSTOM_FILTER`
- X `GROWABLE_NETWORK_TYPE` -> `CARPBI_NETWORK_TYPE`
- X `PBI_CUSTOM_FILTER`
- X `PBI_DICT`
- X `PBI_DICT_SUB`


# SETTINGS
Should probably be tool-specific, if relevant overwrite bnl settings.

# UTILS

## Multi-use
- X `assign_pbi_to_edges()`
- X `get_correct_edgetuples()` -> `nodelist_to_edgetuples()`
- `_get_weighted_distances()`: align gbn-fbn
- `add_point_data_to_net()`: align parameters gbn-fbn
- `create_gdf_with_geoms()`: align gbn-fbn
- `weigh_edges()`: align parameters gbn-fbn, make pbi, length, and weight attributes parameters, make general, include constants.ROUTING_PENALTY
- `bike_infra_mapping_gdf()`: explore how to turn general-purpose

## Single-use
- X gbn: `get_principal_bearing()`, `_reverse_bearing()`, `_count_and_merge()`
- X gbn: `node_to_edge_attributes()`
- X gbn: `route_nodepairs()`: make weight a parameter.
- gbn: `orientation_order()`
- gbn: `add_trip_data_to_net()`: add in future to fbn?
- gbn`_order_df()`: explore how to turn general-purpose
- gbn: `filter_network_by_component_length()`, `prepare_nodes_edges()`: explore how to turn general-purpose
- gbn: `snap_points_to_osm_nodes()`: explore how to turn general-purpose
- gbn: `filter_points_distant_from_osm_nodes()`: explore how to turn general-purpose
- gbn: `set_path_to_pbi()`: make weight a parameter. More general: set path to attribute?



# VIZ
