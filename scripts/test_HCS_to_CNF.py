import sys
import igraph
from HCS_to_CNF import HCS_to_CNF
from cnf_to_edge_set import read_file, cnf_to_edge_set
from test_VIG_to_CNF import isomorphic

depth = int(sys.argv[1])
leaf_community_size = int(sys.argv[2])
# let inter_vars be the density (a fraction of total number of vars in the subgraph)
inter_vars_fraction = float(sys.argv[3])
degree = int(sys.argv[4])
# m is the number of clauses in the CNF
m = int(sys.argv[5])
# k is the width of clauses
k = int(sys.argv[6])
outpath = './' + str(depth) + '_' + str(leaf_community_size) + '_' + str(inter_vars_fraction) + '_' + str(degree) + '_' + str(m) + '_' + str(k) + '.cnf'

HCS_to_CNF(depth, leaf_community_size, inter_vars_fraction, degree, m, k, outpath)

# Check: size of the HCS is equal to the number of variables in the final CNF
clauses, m_out, n_out = read_file(outpath)
if m == m_out and leaf_community_size * (degree ** (depth - 1)) == n_out:
    print("Check 1: PASS \n The size of the HCS is equal to the number of variables in the final CNF")
else:
    print("Check 1: FAIL \n The size of the HCS is NOT equal to the number of variables in the final CNF")

# Check: the output VIG of 1) is isomorphic to the VIG of the output CNF of 2)
if isomorphic('', outpath, m, k):
    print("Check 2: PASS \n The VIG_to_CNF input and output graphs are isomorphic")
else:
    print("Check 2: FAIL \n The VIG_to_CNF input and output graphs are NOT isomorphic")

# Check: visual sanity check for VIG
clauses, temp, n = read_file(outpath)
edge_set = cnf_to_edge_set(clauses)
edge_list = [list(e) for e in edge_set]
g = igraph.Graph()
g.add_vertices(n)
g.add_edges(edge_list)

g.write_svg(outpath[:-4] + '.svg', vertex_size=4, font_size=0)

# Check: total edges is equal to what is expected
# - 8.8 * n = edges in leaf community
# - 3 * intercomm vars = intercomm edges
# - we know how many communities & intercommunity vars
delta_percent_thres = 0.15
total_comm = degree ** (depth - 1)
expected_in_comm = (8.8 * leaf_community_size) * total_comm
level_size = total_comm
total_inter_edges = 0
while level_size > 1:
    total_inter_edges += (3 * inter_vars_fraction * leaf_community_size) * (level_size/degree)
    level_size = level_size/degree

total_expected = int(expected_in_comm + total_inter_edges)

print('Total expected edges: ' + str(total_expected))
print('Total edges found: ' + str(len(g.es())))

if (len(g.es()) - total_expected) < delta_percent_thres * total_expected:
    print("Check 3: PASS \n The total number of edges is what is expected")
else:
    print("Check 3: FAIL \n The total number of edges is NOT what is expected")
