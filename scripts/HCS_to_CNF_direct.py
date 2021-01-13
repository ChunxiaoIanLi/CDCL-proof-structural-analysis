import generate_random_degree_distribution
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import igraph
import sys
import os
import random
import math
import copy
import VIG_to_CNF

def combine_subcnfs(subcnfs):
	community_id_upper_bounds = [0]
	combined_subcnfs = []

	for subcnf in subcnfs:
		largest_var = 0
		for clause in subcnf:
			# Find largest variable in sub-CNF
			largest_var = max(largest_var, max(abs(literal) for literal in clause))

			# Re-number variables in sub-CNF
			combined_subcnfs.append([literal + (-1 if literal < 0 else 1) * community_id_upper_bounds[-1] for literal in clause])

		community_id_upper_bounds.append(community_id_upper_bounds[-1] + largest_var)
	return combined_subcnfs, community_id_upper_bounds

def add_edges_to_combined_disconnected_cnfs(level, depth, inter_vars_fraction, community_id_upper_bounds, k, cnf):
	# Ensure that the actual number of inter-community variables is a multiple of the degree 
	total_vars = community_id_upper_bounds[-1]
	inter_vars = int(total_vars * inter_vars_fraction)
	degree = len(community_id_upper_bounds) - 1
	actual_inter_vars = degree * (inter_vars // degree)

	# Actually add the edges to the CNFs
	return generate_random_degree_distribution.generateRandomInterFormula(community_id_upper_bounds, cvr[level-1], k, cnf, actual_inter_vars)

def generate_VIG(level, depth, leaf_community_size, inter_vars_fraction, degree, k):
	# Generate leaf community
	if level == depth:
		num_clauses    = int(round(leaf_community_size * cvr[-1]))
		uniform_vec    = generate_random_degree_distribution.generateUniformVec   (leaf_community_size, num_clauses, k)
		cumulative_vec = generate_random_degree_distribution.generateCummulative  (uniform_vec)
		leaf_community = generate_random_degree_distribution.generateRandomFormula(leaf_community_size, num_clauses, k, cumulative_vec)
		return leaf_community

	# Generate sub-communities and sub-CNFs
	current_degree = degree[level - 1]
	subcnfs = [
		generate_VIG(level + 1, depth, leaf_community_size, inter_vars_fraction, degree, k)
		for i in range(current_degree)
	]

	# Combine subcommunities into a single graph and update variable names in sub-CNFs accordingly
	combined_disconnected_subcnfs, community_id_upper_bounds = combine_subcnfs(subcnfs)

	# Add inter-community edges and inter-community clauses
	updated_combined_cnf = add_edges_to_combined_disconnected_cnfs(level, depth, inter_vars_fraction, community_id_upper_bounds, k, combined_disconnected_subcnfs)
	return updated_combined_cnf

cvr = [2.0, 2.0, 4.0]

if __name__ == "__main__":
	# Parse arguments
	depth               = int  (sys.argv[1])
	leaf_community_size = int  (sys.argv[2])
	inter_vars_fraction = float(sys.argv[3])
	degree              = int  (sys.argv[4])
	k                   = int  (sys.argv[5])
	out_cnf             = str  (sys.argv[6])
	degree_per_level    = [degree] * (depth - 1)

	# Generate CNF
	final_cnf = generate_VIG(1, depth, leaf_community_size, inter_vars_fraction, degree_per_level, k)

	# Find largest variable
	max_var = max(max(abs(l) for l in c) for c in final_cnf)
	
	# Output CNF
	VIG_to_CNF.write_cnf(final_cnf, max_var, len(final_cnf), out_cnf)

