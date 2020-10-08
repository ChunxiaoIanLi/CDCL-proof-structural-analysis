import igraph
import sys
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import os
import numpy as np
from random import randrange

file = sys.argv[1]

clauses, m, n = read_file(file)
edge_set = cnf_to_edge_set(clauses)
edge_list = [list(e) for e in edge_set]
clauses_list = cnf_to_clauses_list(clauses)


g = igraph.Graph()
g.add_vertices(n)
g.add_edges(edge_list)

layout = g.layout("large")
visual_style = {}
visual_style["layout"] = layout
visual_style["bbox"] = (5000, 5000)
visual_style["vertex_size"] = 1

igraph.plot(g, **visual_style)
