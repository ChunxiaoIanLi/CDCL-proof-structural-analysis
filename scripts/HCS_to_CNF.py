import HCS_to_VIG
import VIG_to_CNF
import sys
import igraph


def g_to_svg(g):
    layout = g.layout("large")
    visual_style = {}
    visual_style["vertex_size"] = 5
    visual_style["layout"] = layout
    visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 10
    # vertex_clustering = g.community_multilevel()
    # igraph.plot(vertex_clustering, "HCS.svg", mark_groups = True, **visual_style)
    igraph.plot(g, "HCS.svg", **visual_style)
    return


def HCS_to_CNF(depth, leaf_community_size, inter_vars_fraction, degree, m, k, outpath):
    # modularity = [0.7, 0.6, 0.5, 0.4]
    degree_per_level = [degree] * (depth - 1)
    print("generating VIG")
    g = HCS_to_VIG.generate_VIG(1, depth, leaf_community_size, inter_vars_fraction, degree_per_level)
    print("VIG generated: {0} nodes {1} edges".format(g.vcount(), g.ecount()))
    g_to_svg(g)
    print("generating CNF")
    cnf = VIG_to_CNF.VIG_to_CNF(g, m, k)
    # VIG_to_CNF.print_cnf(cnf, g.vcount(), m)
    VIG_to_CNF.write_cnf(cnf, g.vcount(), m, outpath)


if __name__ == "__main__":
    depth = int(sys.argv[1])
    leaf_community_size = int(sys.argv[2])
    # let inter_vars be the density (a fraction of total number of vars in the subgraph)
    inter_vars_fraction = float(sys.argv[3])
    degree = int(sys.argv[4])
    # m is the number of clauses in the CNF
    m = int(sys.argv[5])
    # k is the width of clauses
    k = int(sys.argv[6])
    outpath = str(sys.argv[7])

    HCS_to_CNF(depth, leaf_community_size, inter_vars_fraction, degree, m, k, outpath)
