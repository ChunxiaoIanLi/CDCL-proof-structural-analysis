import igraph
import clustering_ed

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

if __name__ == "__main__":
	test_compute_intercommunity_edges()
	test_compute_intercommunity_vars()