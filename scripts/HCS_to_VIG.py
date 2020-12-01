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

def get_zero_adjacency_matrix(n):
	zero_adjacency_matrix = []
	for i in range(n):
		row = [0]*n
		zero_adjacency_matrix.append(row)
	return zero_adjacency_matrix

def combine_adjacency_matrices(subgraphs):
	combined_zero_adjacency_matrix = get_zero_adjacency_matrix(len(subgraphs[0])*len(subgraphs))
	for index in range(len(subgraphs)):
		for each_row in range(len(subgraphs[index])):
			for each_column in range(len(subgraphs[index])):
				combined_zero_adjacency_matrix[index*len(subgraphs[index])+each_row]\
								[index*len(subgraphs[index])+each_column] \
			  	= subgraphs[index][each_row][each_column]

	# At this point, combined_zero_adjacency_matrix is an 
	# all 0 matrix except for the diagonal being the subcommunities to combine
	return combined_zero_adjacency_matrix

def add_edges_to_combined_zero_adjacency_matrix(adjacency_matrix, inter_edges, degree):
	# there are degree**2-degree number of empty cubes in the upper half of the matrix
	# so the expected number of 1's per cube is inter_edges/(degree**2-degree)
	# so the expected number of 1's per row per cube is (inter_edges/(degree**2-degree))/(len(adjacency_matrix)/degree)
	subcommunity_size = len(adjacency_matrix)/degree
	expected_ones_per_cube = inter_edges/(degree**2-degree)
	expected_ones_per_row_per_cube = expected_ones_per_cube/subcommunity_size
	probability_of_edge_per_cell = expected_ones_per_row_per_cube/subcommunity_size
	for index in range(degree-1):
		for each_row in range(subcommunity_size):
			for each_column in range(subcommunity_size):
				if random.random() < probability_of_edge_per_cell:
					adjacency_matrix[index*subcommunity_size+each_row][(index+1)*subcommunity_size+each_column] = 1
					adjacency_matrix[(index+1)*subcommunity_size+each_column][index*subcommunity_size+each_row] = 1
	return adjacency_matrix

def count_inter_vars(adjacency_matrix, degree):
	subcommunity_size = len(adjacency_matrix)/degree
	inter_vars = 0

	# a variable v is an inter-community variable as long as there is
	# a 1 in row adjacency_matrix[v] (except the diagonal)
	for each_row in range(subcommunity_size):
		index = each_row/subcommunity_size
		for each_column in range(len(adjacency_matrix)):
			if adjacency_matrix[each_row][each_column] == 1 and (each_column < index * subcommunity_size or each_column > (index+1) * subcommunity_size):
				inter_vars+=1
				break
	return inter_vars

def compute_modularity(adjacency_matrix, degree):
	g = igraph.Graph.Adjacency(adjacency_matrix)
	membership_list = []
	subcommunity_size = len(adjacency_matrix)/degree
	for i in range(degree):
		for j in range(subcommunity_size):
			membership_list.append(i)
	return g.modularity(membership_list)

def print_matrix(matrix):
	for i in matrix:
		print(i)
	return

def generate_VIG(level, depth, leaf_community_size, inter_vars, inter_edges, modularity, degree):
	current_inter_vars = inter_vars[level-1]
	current_inter_edges = float(inter_edges[level-1])
	current_modularity = float(modularity[level-1])
	current_degree = degree[level-1]
	if level == depth:
		return get_leaf_adjacency_matrix(leaf_community_size)

	subgraphs = []
	for i in range(current_degree):
		subgraphs.append(generate_VIG(level+1, depth, leaf_community_size, inter_vars, inter_edges, modularity, degree))
	
	combined_zero_adjacency_matrix = combine_adjacency_matrices(subgraphs)

	iteration = 1
	# start search for valid matrices 
	while True:
		print(iteration)
		# we add current_inter_edge number of 1's in the matrix (excluding the diagonal)
		updated_adjacency_matrix = add_edges_to_combined_zero_adjacency_matrix(copy.deepcopy(combined_zero_adjacency_matrix), current_inter_edges, current_degree)
		print_matrix(updated_adjacency_matrix)
		# check current_inter_vars
		# switch off
		actual_inter_vars = count_inter_vars(updated_adjacency_matrix, current_degree)
		if (current_inter_vars - 2) < actual_inter_vars and actual_inter_vars < (current_inter_vars + 2):
			# check current_modularity
			# switch off checking for modularity
			# actual_modularity = compute_modularity(updated_adjacency_matrix, current_degree)
			# if (current_modularity - 0.1) < actual_modularity and actual_modularity < (current_modularity + 0.1):
			break
		iteration+=1

	return updated_adjacency_matrix

# have inputs
depth = 5
leaf_community_size = 10
inter_vars = [80, 40, 20, 10, 5]
inter_edges = [480, 240, 120, 60, 30]
modularity = [0.8, 0.6, 0.4, 0.2, 0]
degree = [3, 3, 3, 3, 3]

adjacency_matrix = generate_VIG(1, depth, leaf_community_size, inter_vars, inter_edges, modularity, degree)
g = igraph.Graph.Adjacency(adjacency_matrix)
print(adjacency_matrix)
