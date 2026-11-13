"""Example of bikenetlib used during package development."""

import bikenetlib as bnl
import osmnx as ox

# g=ox.graph_from_point((55.658328, 12.589548), 250)
# ox.io.save_graph_geopackage(g, "osm_network.gpkg")

# print(bnl.utils.get_principal_bearing(g))


g, nodes, edges, boundary_gdf = bnl.io.import_osm_network("osm_network.gpkg", import_path="./tests/test_data/")
