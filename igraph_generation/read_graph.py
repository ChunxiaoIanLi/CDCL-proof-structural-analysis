import sys
import igraph

filename = sys.argv[1]
file = open(filename, 'r')

g = igraph.Graph()
edges = []

for line in file.readlines():
    if line[0] == 'c':
        continue
    if line[0] == 'p':
        tokens = line.split(' ')
        num_vars = tokens[2]
        g.add_vertices(int(num_vars))
        continue

    tokens = line.split(' ')
    edges.append((int(tokens[0]) - 1, int(tokens[1]) - 1))

g.add_edges(edges)
layout = g.layout_lgl()
visual_style = {}
visual_style["layout"] = layout
visual_style["bbox"] = (5000, 5000)
visual_style["vertex_size"] = 20

igraph.plot(g, **visual_style)
