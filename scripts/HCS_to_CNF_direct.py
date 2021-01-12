import generate_random_degree_distribution
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import igraph
import sys
import os
import random
import math
import copy
import VIG_to_CNF

def get_leaf_cnf(n, k, cummulative_vec):
	m = int(n * cvr[-1])
	return generate_random_degree_distribution.generateRandomFormula(n, m, k, cummulative_vec)

def combine_subcnfs(subcnfs):
	community_id_upper_bounds = [0]
	previous_total = 0
	combined_subcnfs = []
	for cnf_index, subcnf in enumerate(subcnfs):
		current_max = 0
		for clause in subcnf:
			for lit_index in range(len(clause)):
				if abs(clause[lit_index]) > current_max:
					current_max = abs(clause[lit_index])
				if clause[lit_index] < 0:
					clause[lit_index] -= previous_total
				else:
					clause[lit_index] += previous_total

		combined_subcnfs += subcnf
		previous_total += current_max
		community_id_upper_bounds.append(previous_total)

	return combined_subcnfs, community_id_upper_bounds

def add_edges_to_combined_disconnected_cnfs(level, depth, inter_vars_fraction, community_id_upper_bounds, k, cnf):
	total_variables   =   community_id_upper_bounds[-1]
	inter_vars        =   int(total_variables*inter_vars_fraction)
	
	degree = len(community_id_upper_bounds) - 1

	mapping = []
	actual_inter_vars = 0
	for i in range(1, degree + 1):
		actual_inter_vars += inter_vars/degree
		random_vars = random.sample(range(community_id_upper_bounds[i-1]+1, community_id_upper_bounds[i]+1), inter_vars/degree)

	cnf = generate_random_degree_distribution.generateRandomInterFormula(community_id_upper_bounds, cvr[level-1], k, cnf, actual_inter_vars)

	return cnf

def generate_VIG(level, depth, leaf_community_size, inter_vars_fraction, degree, k):

	if level == depth:
		uniformvec       =  generate_random_degree_distribution.generateUniformVec(leaf_community_size, leaf_community_size*cvr[-1], k)
		cummulative_vec  =  generate_random_degree_distribution.generateCummulative(uniformvec)
		return get_leaf_cnf(leaf_community_size, k, cummulative_vec)

	current_degree = degree[level-1]

	subcnfs = []
	for i in range(current_degree):
		subcnf = generate_VIG(level+1, depth, leaf_community_size, inter_vars_fraction, degree, k)
		subcnfs.append(subcnf)

	# update variable names in sub-cnfs
	combined_disconnected_subcnfs, community_id_upper_bounds = combine_subcnfs(subcnfs)

	# add inter-community edges and inter-community clauses
	updated_combined_cnf = add_edges_to_combined_disconnected_cnfs(level, depth, inter_vars_fraction, community_id_upper_bounds, k, combined_disconnected_subcnfs)
	return updated_combined_cnf

cnf = []
cvr = [2.0, 2.00, 4.0]

if __name__ == "__main__":
	depth = int(sys.argv[1])
	leaf_community_size = int(sys.argv[2])
	inter_vars_fraction = float(sys.argv[3])
	degree = int(sys.argv[4])
	degree_per_level = [degree]*(depth-1)
	k = int(sys.argv[5])
	outcnf = str(sys.argv[6])

	final_cnf = generate_VIG(1, depth, leaf_community_size, inter_vars_fraction, degree_per_level, k)
	maxvar = 0
	for c in final_cnf:
		for l in c:
			if abs(l) > maxvar:
				maxvar = abs(l)
	VIG_to_CNF.write_cnf(final_cnf, maxvar, outcnf)

