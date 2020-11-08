import igraph

n_s = [1000]
p_s = [0.05]
# Size of the node communities
k_s = [10]

for n in n_s:
    for p in p_s:
        for k in k_s:
            g = igraph.Graph.Erdos_Renyi(n, p)
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

            file = open('n' + str(n) + 'p' + str(int(p * 100)) + 'k' + str(k) + '.cnf', 'w+')
            filelines = ''
            filelines += 'p cnf ' + str(len(g.vs)) + ' ' + str(len(g.es)) + '\n'
            for e in g.es:
                filelines += str(e.source + 1) + ' ' + str(e.target + 1) + ' 0\n'
            file.write(filelines)
            file.close()

            layout = g.layout_lgl()
            visual_style = {}
            visual_style["layout"] = layout
            visual_style["bbox"] = (5000, 5000)
            visual_style["vertex_size"] = 20

            igraph.plot(g, **visual_style)
            # igraph.plot(g)
