from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import igraph
import sys
import os
import random
import math
import copy

# functions to write tests for:
#	1. get_leaf_adjacency_matrix()
#   2. combine_adjacency_matrices()
#   3. add_edges_to_combined_zero_adjacency_matrix()
#   4. count_inter_vars()
#   5. compute_modularity()

def get_leaf_adjacency_matrix(n):
	adjacency_matrix = []
	for i in range(n):
		row = [1]*n
		row[i] = 0
		adjacency_matrix.append(row)
	return adjacency_matrix

def combine_subgraphs(subgraphs):
	current_vertex_count = 0
	total_vertex_count = 0
	community_id_upper_bounds = []
	combined_disconnected_subgraphs = igraph.Graph()

	for g in subgraphs:
		total_vertex_count += g.vcount()
		community_id_upper_bounds.append(total_vertex_count)

	combined_disconnected_subgraphs.add_vertices(total_vertex_count)

	edges_to_add = []
	for i, g in enumerate(subgraphs):
		for e in g.es:
			edges_to_add.append([current_vertex_count+e.source, current_vertex_count+e.target])
		current_vertex_count = community_id_upper_bounds[i]
	combined_disconnected_subgraphs.add_edges(edges_to_add)

	# At this point, combined_zero_adjacency_matrix is an 
	# all 0 matrix except for the diagonal being the subcommunities to combine
	return combined_disconnected_subgraphs, community_id_upper_bounds

def same_community(u, v, community_id_upper_bounds):
	previous = 0
	for current in community_id_upper_bounds:
		if previous <= u < current and previous <= v < current:
			return True
		previous = current
	return False

def pick_inter_triangle(g, u, random_inter_vars, community_id_upper_bounds):
	while True:
		v = random.sample(random_inter_vars, 1)[0]
		if not same_community(u, v, community_id_upper_bounds):
			w = random.sample(random_inter_vars, 1)[0]
			if same_community(u, w, community_id_upper_bounds):
				if g.get_eid(u, w, directed=False, error=False) >= 0:
					return v, w
			elif same_community(v, w, community_id_upper_bounds):
				if g.get_eid(v, w, directed=False, error=False) >= 0:
					return v, w
			else:
				return v, w



def add_edges_to_combined_disconnected_subgraphs(g, inter_vars_fraction, community_id_upper_bounds):

	# randomly pick exactly inter-var number of inter-community variables
	# and add exactly inter-edges number of inter-community edges within the selected variables
	# 	- range(a, b): b is exclusive
	# 	- picking inter_vars distinct variables
	inter_vars = int(g.vcount()*inter_vars_fraction)
	inter_edges = int(inter_vars*math.log(inter_vars)/2)
	while True:
		# phase 1: for each uncovered vertex, connect it to a vertex in another community
		# print("phase 1 starts")
		inter_edges_count = 0
		random_inter_vars = random.sample(range(0, g.vcount()), inter_vars)
		uncovered = set(random_inter_vars)
		# TODO: add an array for edges_to_add and add them all at once
		while len(uncovered) != 0:
			# u is a random vertex in uncovered
			u = uncovered.pop()
			v, w = pick_inter_triangle(g, u, random_inter_vars, community_id_upper_bounds)
			if g.get_eid(u, v, directed=False, error=False) < 0:
				uncovered.discard(v)
				g.add_edge(u, v)
				inter_edges_count+=1
			if g.get_eid(u, w, directed=False, error=False) < 0:
				uncovered.discard(w)
				g.add_edge(u, w)
				inter_edges_count+=1
			if g.get_eid(v, w, directed=False, error=False) < 0:
				uncovered.discard(v)
				uncovered.discard(w)
				g.add_edge(v, w)
				inter_edges_count+=1
		# print("phase 1 done")
		# print("phase 2 started")
		# phase 2: randomly assign the remaining edges
		# TODO: instead of randomly picking u and v, we can fix u first and randomly picking a v from a different community
		if inter_edges >= inter_edges_count:
			while inter_edges - inter_edges_count > 0:
				u = random.sample(random_inter_vars, 1)[0]
				v, w = pick_inter_triangle(g, u, random_inter_vars, community_id_upper_bounds)
				if g.get_eid(u, v, directed=False, error=False) < 0:
					g.add_edge(u, v)
					inter_edges_count+=1
				if g.get_eid(u, w, directed=False, error=False) < 0:
					g.add_edge(u, w)
					inter_edges_count+=1
				if g.get_eid(v, w, directed=False, error=False) < 0:
					g.add_edge(v, w)
					inter_edges_count+=1
			# print("phase 2 done")
			break
	return g

def count_inter_vars(g, community_id_upper_bounds):
	inter_vars = set()
	for e in g.es:
		u = e.source
		v = e.target
		if not same_community(u, v, community_id_upper_bounds):
			# sort and binary search?
			inter_vars.add(u)
			inter_vars.add(v)
	return len(inter_vars)

def compute_modularity(g, community_id_upper_bounds):
	membership_list = []
	previous = 0
	community_index = 0
	for current in community_id_upper_bounds:
		for i in range(current - previous):
			membership_list.append(community_index)
		previous = current
		community_index += 1
	return g.modularity(membership_list)

def print_matrix(matrix):
	for i in matrix:
		print(i)
	return

def generate_VIG(level, depth, leaf_community_size, inter_vars_fraction, degree):
	
	if level == depth:
		# change get leaf community to return an igraph object
		return igraph.Graph.Adjacency(get_leaf_adjacency_matrix(leaf_community_size), mode="UNDIRECTED")

	current_degree = degree[level-1]

	subgraphs = []
	for i in range(current_degree):
		subgraphs.append(generate_VIG(level+1, depth, leaf_community_size, inter_vars_fraction, degree))
	
	combined_disconnected_subgraphs, community_id_upper_bounds = combine_subgraphs(subgraphs)

	#iteration = 1
	# start searching for valid matrices 
	#while True:
	print("level {0}".format(level))
	# we add current_inter_edge number of 1's in the matrix (excluding the diagonal)
	updated_combined_graph = add_edges_to_combined_disconnected_subgraphs(copy.deepcopy(combined_disconnected_subgraphs), inter_vars_fraction, community_id_upper_bounds)
	print("done")
		# 	# check current_modularity
		# 	# switch off checking for modularity
		# 	actual_modularity = compute_modularity(updated_combined_graph, community_id_upper_bounds)
		# 	if abs(current_modularity - actual_modularity) < 0.1:
		# 		break
		#break
		#iteration+=1
	return updated_combined_graph

# have inputs
# need inter_edges > inter_vars*log(inter_vars)/2, log base e.
# experiment 1: fixing the size of graph, vary inter_vars and inter_edges
	# 1.1 fixing inter_vars, scale up inter_edges
	# 1.2 fix inter_edges, scale down inter_vars
# experiment 2: 
# depth = 7
# leaf_community_size = 10
# # let inter_vars be the density (a fraction of total number of vars in the subgraph)
# inter_vars_fraction = 0.3
# degree = [2, 2, 2, 2, 2, 2]
# #modularity = [0.7, 0.6, 0.5, 0.4]


# g = generate_VIG(1, depth, leaf_community_size, inter_vars_fraction, degree)

# layout = g.layout("large")
# visual_style = {}
# visual_style["vertex_size"] = 5
# visual_style["layout"] = layout
# visual_style["bbox"] = (1000, 1000)
# visual_style["margin"] = 10
# vertex_clustering = g.community_multilevel()
# igraph.plot(vertex_clustering, "HCS.svg", mark_groups = True, **visual_style)

#print_matrix(adjacency_matrix)
