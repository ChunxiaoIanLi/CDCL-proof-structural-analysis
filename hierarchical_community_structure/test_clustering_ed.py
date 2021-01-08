import igraph
import clustering_ed
import PMILib
from cnf_to_edge_set import cnf_to_edge_set, cnf_to_clauses_list

def create_clique(nodes):
	edges = []
	for i in range(0, len(nodes) - 1):
		for j in range(i + 1, len(nodes)):
			edges.append([nodes[i], nodes[j]])
	return edges

def test_compute_intercommunity_edges_expect(n, edges, expected_inter_edges):
	g = igraph.Graph()
	g.add_vertices(n)
	g.add_edges(edges)

	inter_edges = clustering_ed.compute_intercommunity_edges(g.community_multilevel())
	if expected_inter_edges != inter_edges:
		print("Expected {}; received {}".format(expected_inter_edges, inter_edges))
		return 1
	return 0

def test_compute_intercommunity_edges():
	test_result = 0
	num_tests = 4

	# Disjoint communities
	test_result += test_compute_intercommunity_edges_expect(6,
		create_clique(range(0, 0 + 2 + 1)) +
		create_clique(range(3, 3 + 2 + 1)),
	0)

	# One edge between communities (depth 1)
	test_result += test_compute_intercommunity_edges_expect(6,
		create_clique(range(0, 0 + 2 + 1)) +
		create_clique(range(3, 3 + 2 + 1)) +
		[[0, 3]],
	1)

	# Two edges between communities (depth 1)
	test_result += test_compute_intercommunity_edges_expect(8,
		create_clique(range(0, 0 + 3 + 1)) +
		create_clique(range(4, 4 + 3 + 1)) +
		[[0, 4], [1, 5]],
	2)

	# Two edges between communities (depth 1)
	test_result += test_compute_intercommunity_edges_expect(8,
		create_clique(range(0, 0 + 3 + 1)) +
		create_clique(range(4, 4 + 3 + 1)) +
		[[0, 4], [1, 4]],
	2)

	print("test_inter_community_edges: {}/{} tests passed".format(num_tests - test_result, num_tests))

def test_compute_intercommunity_vars_expect(n, edges, expected_inter_vars):
	g = igraph.Graph()
	g.add_vertices(n)
	g.add_edges(edges)

	inter_vars = clustering_ed.compute_intercommunity_vars(g, g.community_multilevel())
	if expected_inter_vars != inter_vars:
		print("Expected {}; received {}".format(expected_inter_vars, inter_vars))
		return 1
	return 0

def test_compute_intercommunity_vars():
	test_result = 0
	num_tests = 5

	# Disjoint communities
	test_result += test_compute_intercommunity_vars_expect(6,
		create_clique(range(0, 0 + 2 + 1)) +
		create_clique(range(3, 3 + 2 + 1)),
	0)

	# One edge between communities (depth 1)
	test_result += test_compute_intercommunity_vars_expect(6,
		create_clique(range(0, 0 + 2 + 1)) +
		create_clique(range(3, 3 + 2 + 1)) +
		[[0, 3]],
	2)

	# Two edges between communities (depth 1)
	test_result += test_compute_intercommunity_vars_expect(8,
		create_clique(range(0, 0 + 3 + 1)) +
		create_clique(range(4, 4 + 3 + 1)) +
		[[0, 4], [1, 5]],
	4)

	# Two edges between communities (depth 1)
	test_result += test_compute_intercommunity_vars_expect(8,
		create_clique(range(0, 0 + 3 + 1)) +
		create_clique(range(4, 4 + 3 + 1)) +
		[[0, 4], [1, 4]],
	3)

	# Two edges between communities (depth 1)
	test_result += test_compute_intercommunity_vars_expect(8,
		create_clique(range(0, 0 + 3 + 1)) +
		create_clique(range(4, 4 + 3 + 1)) +
		[[0, 4], [0, 5]],
	3)

	print("test_inter_community_vars: {}/{} tests passed".format(num_tests - test_result, num_tests))

def test_compute_hierarchical_community_structure_expect(n, clauses,
	expected_mergeability1norm1_data,
	expected_mergeability1norm2_data,
	expected_mergeability2norm1_data,
	expected_mergeability2norm2_data,
	expected_modularity_data,
	expected_degree_data,
	expected_community_size_data,
	expected_inter_edges_data,
	expected_inter_vars_data,
	expected_pre_width_data,
	expected_post_width_data,
	expected_cvr_data
):
	# Initialize graphs
	g = igraph.Graph()
	g.add_vertices(n)
	g.add_edges([list(e) for e in cnf_to_edge_set(clauses)])
	for i in range(n): g.vs[i]['name'] = i

	hierarchical_tree = igraph.Graph()
	hierarchical_tree.add_vertices(1)
	current_node = 0
	path = [0]

	# Initialize data structures
	pmi = PMILib.PMI()
	pmi.setClauses(cnf_to_clauses_list(clauses))
	output_directory = "/dev/null/"
	mergeability1norm1_data = []
	mergeability1norm2_data = []
	mergeability2norm1_data = []
	mergeability2norm2_data = []
	modularity_data         = []
	degree_data             = []
	community_size_data     = []
	inter_edges_data        = []
	inter_vars_data         = []
	pre_width_data          = []
	post_width_data         = []
	cvr_data                = []
	
	# Run computation
	clustering_ed.compute_hierarchical_community_structure(
		g, hierarchical_tree, current_node, path, pmi,
		mergeability1norm1_data, mergeability1norm2_data, mergeability2norm1_data, mergeability2norm2_data,
		modularity_data, degree_data, community_size_data, inter_edges_data, inter_vars_data,
		pre_width_data, post_width_data, cvr_data, output_directory
	)

	result = 0
	if (mergeability1norm1_data != expected_mergeability1norm1_data):
		result += 1
		print("[mergeability1norm1_data] Test failed: received {}; expected {}".format(mergeability1norm1_data, expected_mergeability1norm1_data))
	if (mergeability1norm2_data != expected_mergeability1norm2_data):
		result += 1
		print("[mergeability1norm2_data] Test failed: received {}; expected {}".format(mergeability1norm2_data, expected_mergeability1norm2_data))
	if (mergeability2norm1_data != expected_mergeability2norm1_data):
		result += 1
		print("[mergeability2norm1_data] Test failed: received {}; expected {}".format(mergeability2norm1_data, expected_mergeability2norm1_data))
	if (mergeability2norm2_data != expected_mergeability2norm2_data):
		result += 1
		print("[mergeability2norm2_data] Test failed: received {}; expected {}".format(mergeability2norm2_data, expected_mergeability2norm2_data))
	if (modularity_data != expected_modularity_data):
		result += 1
		print("[modularity_data        ] Test failed: received {}; expected {}".format(modularity_data        , expected_modularity_data        ))
	if (degree_data != expected_degree_data):
		result += 1
		print("[degree_data            ] Test failed: received {}; expected {}".format(degree_data            , expected_degree_data            ))
	if (community_size_data != expected_community_size_data):
		result += 1
		print("[community_size_data    ] Test failed: received {}; expected {}".format(community_size_data    , expected_community_size_data    ))
	if (inter_edges_data != expected_inter_edges_data):
		result += 1
		print("[inter_edges_data       ] Test failed: received {}; expected {}".format(inter_edges_data       , expected_inter_edges_data       ))
	if (inter_vars_data != expected_inter_vars_data):
		result += 1
		print("[inter_vars_data        ] Test failed: received {}; expected {}".format(inter_vars_data        , expected_inter_vars_data        ))
	if (pre_width_data != expected_pre_width_data):
		result += 1
		print("[pre_width_data         ] Test failed: received {}; expected {}".format(pre_width_data         , expected_pre_width_data         ))
	if (post_width_data != expected_post_width_data):
		result += 1
		print("[post_width_data        ] Test failed: received {}; expected {}".format(post_width_data        , expected_post_width_data        ))
	if (cvr_data != expected_cvr_data):
		result += 1
		print("[cvr_data               ] Test failed: received {}; expected {}".format(cvr_data               , expected_cvr_data               ))
	return result

def test_compute_hierarchical_community_structure():
	test_result = 0
	num_tests = 2 * 12
	nan = float("nan")

	# Single community
	test_result += test_compute_hierarchical_community_structure_expect(3,
		[[1, 2, 3]],
		[[str(nan)]],
		[[str(0.0)]],
		[[str(nan)]],
		[[str(0.0)]],
		[[str(0.0)]],
		[[str(1)]],
		[[str(3)]],
		[[str(0)]],
		[[str(0)]],
		[[str(3.0)]],
		[[str(0.0)]],
		[[str(1/3.)]]
	)

	# Disjoint communities
	test_result += test_compute_hierarchical_community_structure_expect(6,
		[[1, 2, 3], [4, 5, 6]],
		[[str(nan) ], [str(nan) , str(nan) ]],
		[[str(0.0) ], [str(0.0) , str(0.0) ]],
		[[str(nan) ], [str(nan) , str(nan) ]],
		[[str(0.0) ], [str(0.0) , str(0.0) ]],
		[[str(0.5) ], [str(0.0) , str(0.0) ]],
		[[str(2)   ], [str(1)   , str(1)   ]],
		[[str(6)   ], [str(3)   , str(3)   ]],
		[[str(0)   ], [str(0)   , str(0)   ]],
		[[str(0)   ], [str(0)   , str(0)   ]],
		[[str(3.0) ], [str(3.0) , str(3.0) ]],
		[[str(0.0) ], [str(0.0) , str(0.0) ]],
		[[str(2/6.)], [str(1/3.), str(1/3.)]]
	)

	print("test_inter_community_edges: {}/{} tests passed".format(num_tests - test_result, num_tests))

if __name__ == "__main__":
	test_compute_intercommunity_edges()
	test_compute_intercommunity_vars()
	test_compute_hierarchical_community_structure()