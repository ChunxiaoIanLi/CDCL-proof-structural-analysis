import generate_random_degree_distribution
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import igraph
import sys
import os
import random
import math
import copy
import VIG_to_CNF

# returns the largest variable in a cnf
def get_n(cnf):
	n = 0
	for c in final_cnf:
		for l in c:
			if abs(l) > n:
				n = abs(l)
	return n

def get_leaf_cnf(n, k, cummulative_vec):
	m = int(n * cvr[-1])
	return generate_random_degree_distribution.generateRandomFormula(n, m, k, cummulative_vec)

# input:
#	subcnfs                    :   subcnfs is a 2D array, where each element in subcnf is a cnf corresponding to a sub-community
#			 					   subcnfs = [cnf1, cnf2, cnf3, cnf4, ...], at this point all sub-cnfs starts from variable 1
# output:
#	combined_subcnfs           :   a cnf whose number of clauses equals to the sum of all clauses from subcnfs
#					  			   note that combined_subcnfs does not contain inter-community clauses yet
#	community_id_upper_bounds  :   an array of non-negative integers [0, x, y, z, ...] where x is the
#   						       size of community 1, y-x is the size of community 2, and z-x is the
#   						       size of community 3
def combine_subcnfs(subcnfs):
	community_id_upper_bounds = [0]
	# previous total is the number of variables we have seen, so to add another subcnf
	# we need to increase every variable in that subcnf by previous_total
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

# inputs:
#   level                      :   current level in the recursion
#   depth-1 				   :   the overall depth
#   inter_vars_fraction		   :   the portion of variables in a subcommunity that are inter community variables		
#   community_id_upper_bounds  :   an array of non-negative integers [0, x, y, z, ...] where x is the
#   						       size of community 1, y-x is the size of community 2, and z-x is the
#   						       size of community 3
#   k 						   :   clause width
#   cnf 					   :   the current formula which we will add inter-community clauses to
#outputs:
#   cnf 					   :   the cnf with inter-community clauses added
def add_edges_to_combined_disconnected_cnfs(level, depth, inter_vars_fraction, community_id_upper_bounds, k, cnf):
	total_variables   =   community_id_upper_bounds[-1]
	inter_vars        =   int(total_variables*inter_vars_fraction)
	degree 			  =   len(community_id_upper_bounds) - 1

	actual_inter_vars = 0
	# for each sub-community c, pick size(c)*inter_var_fraction number of inter-community variables
	for i in range(1, degree + 1):
		actual_inter_vars += inter_vars/degree
		# random_vars = random.sample(range(community_id_upper_bounds[i-1]+1, community_id_upper_bounds[i]+1), inter_vars/degree)

	cnf = generate_random_degree_distribution.generateRandomInterFormula(community_id_upper_bounds, cvr[level-1], k, cnf, actual_inter_vars)

	return cnf

# generates a HCS formula from bottom up
# inputs: 
# 	level 					   :   current level in the recursion
# 	depth                      :   the overall depth
# 	leaf_community_size        :   number of variables in leave communities
# 	inter_vars_fraction		   :   the portion of variables in a subcommunity that are inter community variables
# 	degree 					   :   degree for each level of the hierarchy
# 	k 						   :   clause width
# outputs:
# 	updated_combined_cnf   	   :   the cnf which corresponds to the HCS
def generate_VIG(level, depth, leaf_community_size, inter_vars_fraction, degree_per_level, k):
	# base case of the recursion, if we are at the leaf communities, then simply return
	# a random k-cnf formula of leaf_community_size number of variables with cvr blah
	# cvr is currenlty a global variable which is accessed inside get_leaf_cnf()
	if level == depth:
		uniformvec       =  generate_random_degree_distribution.generateUniformVec(leaf_community_size, leaf_community_size*cvr[-1], k)
		cummulative_vec  =  generate_random_degree_distribution.generateCummulative(uniformvec)
		return get_leaf_cnf(leaf_community_size, k, cummulative_vec)

	# if we are not at the base case, current_degree is the number of sub-communities to combine
	current_degree = degree_per_level[level-1]
	# subcnfs is a 2D array, where each element in subcnf is a cnf corresponding to a sub-community
	subcnfs = []
	for i in range(current_degree):
		# get the sub-formula for each sub-community
		subcnf = generate_VIG(level+1, depth, leaf_community_size, inter_vars_fraction, degree_per_level, k)
		subcnfs.append(subcnf)

	# subcnfs = [cnf1, cnf2, cnf3, cnf4, ...], at this point all sub-cnfs starts from variable 1
	# combine_subcnfs() updates variable names in sub-cnfs, so we can combine all of them into one cnf
	combined_disconnected_subcnfs, community_id_upper_bounds = combine_subcnfs(subcnfs)

	# add inter-community edges and inter-community clauses
	updated_combined_cnf = add_edges_to_combined_disconnected_cnfs(level, depth, inter_vars_fraction, community_id_upper_bounds, k, combined_disconnected_subcnfs)
	return updated_combined_cnf

cvr = [2.0, 2.00, 4.0]

if __name__ == "__main__":
	depth               = int(sys.argv[1])
	leaf_community_size = int(sys.argv[2])
	inter_vars_fraction = float(sys.argv[3])
	degree              = int(sys.argv[4])
	degree_per_level    = [degree]*(depth-1)
	k				    = int(sys.argv[5])
	outcnf              = str(sys.argv[6])

	final_cnf = generate_VIG(1, depth, leaf_community_size, inter_vars_fraction, degree_per_level, k)
	n = get_n(cnf)
	VIG_to_CNF.write_cnf(final_cnf, n, outcnf)

