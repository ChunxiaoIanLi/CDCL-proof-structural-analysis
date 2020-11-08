import igraph

n_s = [10, 100, 1000]
p_s = [0.1, 0.5, 0.9]
# Size of the node communities
k_s = [3, 4]

for n in n_s:
    for p in p_s:
        for k in k_s:
            g = igraph.Graph.Erdos_Renyi(n, p)
            v_s = [vertex.index for vertex in g.vs]
            original_v_count = len(v_s)
            for v in v_s:
                g.add_vertices(k)
                new_v_start = original_v_count + v * k
                new_v_end = original_v_count + (v + 1) * k - 1
                g.add_edges([(v, new_v_start)])
                new_v_index = new_v_start
                while new_v_index < new_v_end:
                    for v2 in range(new_v_index + 1, new_v_end + 1):
                        g.add_edges([(new_v_index, v2)])
                    new_v_index += 1

            file = open('n' + str(n) + 'p' + str(int(p * 100)) + 'k' + str(k) + '.cnf', 'w+')
            file.write('p cnf ' + str(len(g.vs)) + ' ' + str(len(g.es)) + '\n')
            for e in g.es:
                file.write(str(e.source) + ' ' + str(e.target) + ' 0\n')
            file.close()
            igraph.plot(g)
