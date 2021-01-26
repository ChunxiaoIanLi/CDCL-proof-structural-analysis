import generate_random_degree_distribution
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
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

# inputs:
#   level                      :   current level in the recursion
#   depth-1 				   :   the overall depth
#	offset                     :   the variable ID offset for the current community
#	degree_vector              :   the degree vector
#   inter_vars_fraction		   :   the portion of variables in a subcommunity that are inter community variables		
#   community_id_upper_bounds  :   an array of non-negative integers [0, x, y, z, ...] where x is the
#   						       size of community 1, y-x is the size of community 2, and z-x is the
#   						       size of community 3
#   k 						   :   clause width
#   cnf 					   :   the current formula which we will add inter-community clauses to
# outputs:
#   cnf 					   :   the cnf with inter-community clauses added
def add_edges_to_combined_disconnected_cnfs(level, depth, offset, degree_vector, inter_vars_fraction, community_id_upper_bounds, k, cnf, cvr):
	# Ensure that the actual number of inter-community variables is a multiple of the degree 
	total_vars = community_id_upper_bounds[-1]
	inter_vars = int(total_vars * inter_vars_fraction)
	degree = len(community_id_upper_bounds) - 1
	actual_inter_vars = degree * (inter_vars // degree)

	# Actually add the edges to the CNFs
	return generate_random_degree_distribution.generateRandomInterFormula(offset, degree_vector, community_id_upper_bounds, cvr[level-1], k, cnf, actual_inter_vars)

def generate_VIG(level, depth, offset, degree_vector, leaf_community_size, inter_vars_fraction, degree, k, cvr):
	# Generate leaf community
	if level == depth:
		num_clauses    = int(round(leaf_community_size * cvr[-1]))
		leaf_degree_vec = degree_vector[offset : offset + leaf_community_size]
		leaf_community = generate_random_degree_distribution.generateRandomFormula(leaf_community_size, num_clauses, k, leaf_degree_vec)
		return leaf_community

	# Generate sub-communities and sub-CNFs
	current_degree = degree[level - 1]
	vars_per_subtree = leaf_community_size
	for deg in degree[level:]: vars_per_subtree *= deg
	subcnfs = [
		generate_VIG(level + 1, depth, offset + i * vars_per_subtree, degree_vector, leaf_community_size, inter_vars_fraction, degree, k, cvr)
		for i in range(current_degree)
	]

	# Combine subcommunities into a single graph and update variable names in sub-CNFs accordingly
	combined_disconnected_subcnfs, community_id_upper_bounds = combine_subcnfs(subcnfs)

	# Add inter-community edges and inter-community clauses
	updated_combined_cnf = add_edges_to_combined_disconnected_cnfs(
		level, depth, offset, degree_vector, inter_vars_fraction,
		community_id_upper_bounds, k, combined_disconnected_subcnfs, cvr
	)
	return updated_combined_cnf

if __name__ == "__main__":
	# Parse arguments
	depth               = int  (sys.argv[1])
	leaf_community_size = int  (sys.argv[2])
	inter_vars_fraction = float(sys.argv[3])
	degree              = int  (sys.argv[4])
	k                   = int  (sys.argv[5])
	out_cnf             = str  (sys.argv[6])
	degree_per_level    = [degree] * (depth - 1)

	# cvr
	leaf_cvr = 4.1
	cvr = [(i + 1) * leaf_cvr / depth for i in range(depth)]
	
	# Calculate total number of variables
	num_leaf_communities = 1
	for i, deg in enumerate(degree_per_level):
		num_leaf_communities *= deg
	n = leaf_community_size * num_leaf_communities

	# Generate CNF
	beta = 2.3
	degree_vector = generate_random_degree_distribution.generatePowerlawVecFromBeta(n, beta)
	final_cnf = generate_VIG(1, depth, 0, degree_vector, leaf_community_size, inter_vars_fraction, degree_per_level, k, cvr)
	
	# Output CNF
	VIG_to_CNF.write_cnf(final_cnf, n, out_cnf)

