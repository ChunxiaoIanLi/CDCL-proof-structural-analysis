import sys
import math
import os
import random

# generates a uniform degree vector with n variables, m clauses and width k
def generateUniformVec(n, m, k):
	"""
	Generate a uniform degree vector where variable occurences are distributed evenly
	"""
	total_degree = m * k
	avg          = int(total_degree / n)
	remainder    = int(total_degree % n)
	vec          = [avg] * n
	for i in range(0, remainder): vec[i] += 1
	return vec

# generates a powerlaw degree vector with n variables, m clauses and width k
def generatePowerlawVec(n, m, k):
	"""
	Generate an unbalanced degree vector
	Important note: this does not actually generate a powerlaw degree vector
	"""
	total_degree = m * k
	if total_degree < n: return [1] * (total_degree) + [0] * (n - total_degree)
	avg       = int((total_degree - n) / int(n / 2))
	remainder = int((total_degree - n) % int(n / 2))
	vec = [1] * n
	for i in range(int(n / 2)): vec[i] += avg
	for i in range(remainder):  vec[i] += 1

	return vec

# generates a powerlaw degree vector with n variables and powerlaw beta
def generatePowerlawVecFromBeta(n, beta):
	"""
	Generate a powerlaw degree vector
	Powerlaw is defined as: the fraction of vertices of degree k is proportional to k^(-beta)
	"""
	return [(1 + i)**(-beta) for i in range(n)]

# generates a degree vector with n variables, m clauses and width k that is not too balanced and
# also not too unbalanced
def generateMediumVec(n, m, k):
	vec = generatePowerlawVec(n, m, k)
	max_degree = vec[0] - 2
	for i in range(n // 2):
		diff = random.randint(0, max_degree)
		vec[ i    ] -= diff
		vec[-i - 1] += diff
	return vec

# input:
#   vec                     :   a degree vector [a, b, c, d, ...]
# output:
#   cumulative_vec         :   [a, a+b, a+b+c, a+b+c+d, ...]
def generateCummulative(vec):
	if len(vec) == 0: return []
	cumulative_vec = [vec[0]]
	for i in vec[1:]: cumulative_vec.append(i + cumulative_vec[-1])
	return cumulative_vec

# assigns the polarity of var randomly
def var_to_lit(var):
	# Select a variable with a random polarity
	return var if random.randint(0, 1) else var * -1

def get_lit(degree_vec):
	# Sample literal according to the degree distribution
	var = random.choices(population=range(len(degree_vec)), weights=degree_vec)[0] + 1
	return var_to_lit(var)

# input:
#   tmp_clause              :   an array that either conains zero or one integer
#   k                       :   clause width
#   degree_vec              :   the degree vector [a, b, c, d, ...] 
# output:
#   tmp_clause              :   an intra-community clause of width k
def get_k_lits(tmp_clause, k, degree_vec):
	# Sample distinct variables until the clause is size k
	while len(tmp_clause) < k:
		while True:
			lit = get_lit(degree_vec)
			if (lit not in tmp_clause) and (-lit not in tmp_clause): break
		tmp_clause.append(lit)
	
	# Sort clause for easy comparison
	tmp_clause.sort()
	return tmp_clause

# input:
#   cnf                         :   A 2D array of clauses
#   clause                      :   an array that either conains zero or one integer
#   k                           :   clause width
#   degree_vec                  :   the degree vector [a, b, c, d, ...] 
# output:
#   cnf                         :   the input cnf with one more clause
def get_new_clause(cnf, clause, k, degree_vec):
	# Sample a new clause of size k
	while True:
		tmp_clause = get_k_lits(clause[:], k, degree_vec)
		if tmp_clause not in cnf: return tmp_clause

def get_community(v, community_id_upper_bounds):
	# Get the largest upper bound less than the variable
	for i, upper_bound in enumerate(community_id_upper_bounds):
		if v <= upper_bound: return community_id_upper_bounds[i - 1]

# input:
#   lits                        :   a vector of literals
#   community_id_upper_bounds   :   an array of non-negative integers [0, x, y, z, ...] where x is the
#                                   size of community 1, y-x is the size of community 2, and z-x is the
#                                   size of community 3
# output:
#   result                      :   True if all the literals in liters are from the same community,
#                                   False otherwise
def all_same_community(lits, community_id_upper_bounds):
	# Determine if all literals are in the same community
	if len(lits) <= 1: return True
	required_community = get_community(abs(lits[0]), community_id_upper_bounds)
	return all(required_community == get_community(abs(lit), community_id_upper_bounds) for lit in lits)

def add_var_from_degree_vector(var_set, variables, degree_vector):
	while True:
		i = random.choices(range(len(variables)), degree_vector)[0]
		new_var = variables[i]
		degree_vector[i] = 0 # Select without replacement
		if new_var not in var_set and -new_var not in var_set: break
	var_set.append(new_var)
	return var_set

def add_lit_from_degree_vector(clause, variables, degree_vector):
	while True:
		i = random.choices(range(len(variables)), degree_vector)[0]
		new_var = variables[i]
		degree_vector[i] = 0 # Select without replacement
		if new_var not in clause and -new_var not in clause: break
	clause.append(var_to_lit(new_var))
	return clause

def select_from_random_communities(clause, com_degree_vector, inter_vars, k, community_id_upper_bounds):
	# Ensure that the clause is non-empty
	com_degree_vector_copy = com_degree_vector[:]
	if not clause: clause = add_lit_from_degree_vector(clause, inter_vars, com_degree_vector_copy)
	first_community = get_community(abs(clause[0]), community_id_upper_bounds)

	# Modify weights to ensure we select a variable from a different community
	for i in range(len(com_degree_vector_copy)):
		if get_community(inter_vars[i], community_id_upper_bounds) == first_community:
			com_degree_vector_copy[i] = 0
	
	# Sample a variable from a different community
	tmp_clause = add_lit_from_degree_vector(clause[:], inter_vars, com_degree_vector_copy)
	assert(not all_same_community(tmp_clause, community_id_upper_bounds))

	# Randomly sample variables from random communities
	com_degree_vector_copy = com_degree_vector[:]
	while len(tmp_clause) < k:
		add_lit_from_degree_vector(tmp_clause, inter_vars, com_degree_vector_copy)
	tmp_clause.sort()
	return tmp_clause

# fill clause with k random chosen literals
# reroll if all literals are from the same community
# input:
#   cnf                         :   A 2D array of clauses
#   clause                      :   an array that either conains zero or one integer
#	com_degree_vector           :   the subset of the degree vector containing only the degrees of the
#                                   inter-community variables
#   inter_vars_per_community    :   A 2D array where the i'th element is an array containing the
#                                   inter-community variables from the i'th community
#   k                           :   clause width
#   community_id_upper_bounds   :   an array of non-negative integers [0, x, y, z, ...] where x is the
#                                   size of community 1, y-x is the size of community 2, and z-x is the
#                                   size of community 3
# output:
#   temp_clause                 :   an inter-community clause of width k
def select_inter_vars(cnf, clause, com_degree_vector, inter_vars, k, community_id_upper_bounds):
	while True:
		# Randomly sample variables from random communities, according to degree distribution
		tmp_clause = select_from_random_communities(clause[:], com_degree_vector, inter_vars, k, community_id_upper_bounds)

		# Check if the clause is eligible to be be put into the CNF
		if tmp_clause not in cnf: return tmp_clause

def generateRandomFormula(n, m, k, degree_vec):
	cnf = []
	# Phase 1: make sure every variable is covered
	for i in range(min(n, m)): cnf.append(get_new_clause(cnf, [var_to_lit(i + 1)], k, degree_vec))
	# Phase 2: add additional clauses according to degree distribution
	for i in range(m - n): cnf.append(get_new_clause(cnf, [     ], k, degree_vec))
	return cnf

# this function is for generating inter-community clauses
# input:
#	offset                     :   the variable ID offset for the current community
#	degree_vector              :   the degree vector
#   community_id_upper_bounds   :   an array of non-negative integers [0, x, y, z, ...] where x is the
#                                   size of community 1, y-x is the size of community 2, and z-x is the
#                                   size of community 3 
#   cvr                         :   clause variable ratio
#   k                           :   clause width
#   cnf                         :   all the clauses we have so far
#   inter_vars                  :   total number of inter_community variables
# output:
#   cnf                         :   contains intra-community clauses and inter-community clauses
def generateRandomInterFormula(offset, degree_vector, community_id_upper_bounds, cvr, k, cnf, num_inter_vars):
	# Select inter-community variables according to degree vector
	degree = len(community_id_upper_bounds) - 1
	inter_vars = []
	for i in range(degree):
		curr_community_inter_vars = []
		community_vars = range(community_id_upper_bounds[i] + 1, community_id_upper_bounds[i + 1] + 1)
		community_degree_vector = list(degree_vector[offset + community_id_upper_bounds[i] : offset + community_id_upper_bounds[i + 1]])
		for j in range(num_inter_vars // degree):
			add_var_from_degree_vector(curr_community_inter_vars, community_vars, community_degree_vector)
		inter_vars += curr_community_inter_vars

	# Generate the subset of the degree vector containing only the degrees of the inter-community variables
	com_degree_vector = [degree_vector[offset + iv - 1] for iv in inter_vars]

	# Phase 1: make sure every inter-community variable appears in some clause
	for iv in inter_vars:
		cnf.append(select_inter_vars(cnf, [var_to_lit(iv)], com_degree_vector, inter_vars, k, community_id_upper_bounds))

	# Phase 2: distribute the remaining clauses randomly amongst the intercommunity variables
	for c in range(int(degree * (num_inter_vars // degree) * cvr) - len(inter_vars)):
		cnf.append(select_inter_vars(cnf, [], com_degree_vector, inter_vars, k, community_id_upper_bounds))

	return cnf