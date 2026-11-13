"""Example of bikenetlib used during package development."""

import bikenetlib as bnl
import osmnx as ox

g=ox.graph_from_bbox((12.581039,55.656105,12.596692,55.661062))
ox.io.save_graph_geopackage(g, "osm_network.gpkg")

print(bnl.utils.get_principal_bearing(g))


g, nodes, edges, boundary_gdf = bnl.io.import_osm_network("osm_network.gpkg", import_path="./tests/test_data/")
