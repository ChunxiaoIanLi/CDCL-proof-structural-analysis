import igraph
import networkx as nx
import random
import sys
import math

random.seed(2323)

n_s = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

for n in n_s:
    k = int(math.log(n))

    gp = nx.random_regular_graph(k, n, 2323)

    e = []
    g = igraph.Graph()

    for (u, v) in gp.edges():
        e.append((u, v))

    g.add_vertices(n)
    g.add_edges(e)

    # g = igraph.Graph.Erdos_Renyi(n, p)

    if k > 0:
        v_s = [vertex.index for vertex in g.vs]
        original_v_count = len(v_s)
        for v in v_s:
            g.add_vertices(k - 1)
            new_v_start = original_v_count + v * (k - 1)
            new_v_end = original_v_count + (v + 1) * (k - 1)
            # Connect new nodes with v
            for original_v_index in range(new_v_start, new_v_end):
                g.add_edges([(v, original_v_index)])
            # Connect new nodes with each other
            new_v_index = new_v_start
            while new_v_index < new_v_end - 1:
                for v2 in range(new_v_index + 1, new_v_end):
                    g.add_edges([(new_v_index, v2)])
                new_v_index += 1

    file = open('n' + str(n) + 'k' + str(k) + '.cnf', 'w+')
    filelines = ''
    filelines += 'p cnf ' + str(len(g.vs)) + ' ' + str(len(g.es)) + '\n'
    for e in g.es:
        filelines += str(e.source + 1) + ' ' + str(e.target + 1) + ' 0\n'
    file.write(filelines)
    file.close()

    if len(sys.argv) > 1 and sys.argv[1] == 'plot':
        layout = g.layout_lgl()
        visual_style = {}
        visual_style["layout"] = layout
        visual_style["bbox"] = (5000, 5000)
        visual_style["vertex_size"] = 20

        igraph.plot(g, **visual_style)
