# CONSTANTS
General constants.

## Single-use
- gbn: `_BEARING_BINS`

## Multi-use
- `_ROUTING_PENALTY`
- `_PROGRESS_BAR_DESC_LENGTH`
- `_PROGRESS_BAR_LENGTH`


# IO
Input/Output like downloads, imports, exports, but also format conversions and user feedback tools.

## Multi-use
- `slugify()`
- `initialize_progress_bar()`: require tqdm
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
- import custom tags
- `GROWABLE_NETWORK_CUSTOM_FILTER` -> `CAR_AND_PBI_NETWORK_CUSTOM_FILTER`
- `GROWABLE_NETWORK_TYPE` -> `CAR_AND_PBI_NETWORK_TYPE`
- `PBI_CUSTOM_FILTER`
- `PBI_DICT`
- `PBI_DICT_SUB`


# SETTINGS
Should probably be tool-specific, if relevant overwrite bnl settings.

# UTILS

## Multi-use
- `assign_pbi_to_edges()`
- `get_correct_edgetuples()` -> `nodelist_to_edgetuples()`
- `_get_weighted_distances()`: align gbn-fbn
- `add_point_data_to_net()`: align parameters gbn-fbn
- `create_gdf_with_geoms()`: align gbn-fbn
- `weigh_edges()`: align parameters gbn-fbn, make pbi, length, and weight attributes parameters, make general
- `bike_infra_mapping_gdf()`: explore how to turn general-purpose

## Single-use
- gbn: `get_principal_bearing()`, `_reverse_bearing()`, `_count_and_merge()`
- gbn: `node_to_edge_attributes()`: add an attribute name parameter.
- gbn: `route_nodepairs()`: make weight a parameter.
- gbn: `add_trip_data_to_net()`: add in future to fbn?
- gbn`_order_df()`: explore how to turn general-purpose
- gbn: `filter_network_by_component_length()`, `prepare_nodes_edges()`: explore how to turn general-purpose
- gbn: `snap_points_to_osm_nodes()`: explore how to turn general-purpose
- gbn: `filter_points_distant_from_osm_nodes()`: explore how to turn general-purpose
- gbn: `set_path_to_pbi()`: make weight a parameter. More general: set path to attribute?



# VIZ
