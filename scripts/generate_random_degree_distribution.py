import sys
import math
import os
import random

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

def generateMediumVec(n, m, k):
    #somehow vec[0] is not modified after this call?
	vec = generatePowerlawVec(n, m, k)
	max_degree = vec[0] - 2
	for i in range(int(n / 2)):
		diff = random.randint(0, max_degree)
		vec[ i] -= diff
		vec[-i] += diff
	return vec

def generateCummulative(vec):
	cumulative_vec = [vec[0]]
	for i in vec[1:]: cumulative_vec.append(i + cumulative_vec[-1])
	return cumulative_vec

def var_to_lit(var):
	# Select a variable with a random polarity
	return var if random.randint(0, 1) else var * -1

def get_lit(cumulative_vec, m, k):
	# Sample literal according to the degree distribution
	r = random.randint(0, m * k)
	for i, cumulative_sum in enumerate(cumulative_vec):
		if r <= cumulative_sum: return var_to_lit(i + 1)

	# The program should never get here!
	assert False

def get_k_lits(tmp_clause, m, k, cumulative_vec):
	# Sample distinct variables until the clause is size k
	while len(tmp_clause) < k:
		while True:
			lit = get_lit(cumulative_vec, m, k)
			if (lit not in tmp_clause) and (-lit not in tmp_clause): break
		tmp_clause.append(lit)
	
	# Sort clause for easy comparison
	tmp_clause.sort()
	return tmp_clause

def get_new_clause(cnf, clause, m, k, cumulative_vec):
	# Sample a new clause of size k
	while True:
		tmp_clause = get_k_lits(clause[:], m, k, cumulative_vec)
		if tmp_clause not in cnf: return tmp_clause

def get_community(v, community_id_upper_bounds):
	# Get the largest upper bound less than the variable
	for i, upper_bound in enumerate(community_id_upper_bounds):
		if v < upper_bound: return community_id_upper_bounds[i - 1]

def all_same_community(lits, community_id_upper_bounds):
	# Determine if all literals are in the same community
	if len(lits) == 0: return True
	required_community = get_community(lits[0], community_id_upper_bounds)
	return all(get_community(lit, community_id_upper_bounds) for lit in lits)

def select_from_random_communities(clause, inter_vars_per_community, k):
	# Randomly sample variables from random communities
	tmp_clause = clause[:]
	while len(tmp_clause) < k:
		random_comm = random.randint(0, len(inter_vars_per_community) - 1)
		random_var = random.sample(inter_vars_per_community[random_comm], 1)[0]
		tmp_clause.append(var_to_lit(random_var))
	tmp_clause.sort()
	return tmp_clause

def select_inter_vars(cnf, clause, inter_vars_per_community, k, community_id_upper_bounds):
    while True:
		# Randomly sample variables from random communities
		# In the future: sample variables according to degree distribution
        tmp_clause = select_from_random_communities(clause, inter_vars_per_community, k)

		# Check if the clause is eligible to be be put into the CNF
        if (not all_same_community(tmp_clause, community_id_upper_bounds)) and (tmp_clause not in cnf):
			return tmp_clause

def generateRandomFormula(n, m, k, cumulative_vec):
	cnf = []
	# Phase 1: make sure every variable is covered
	for i in range(n    ): cnf.append(get_new_clause(cnf, [i + 1], m, k, cumulative_vec))
	# Phase 2: add additional clauses according to degree distribution
	for i in range(m - n): cnf.append(get_new_clause(cnf, [     ], m, k, cumulative_vec))
	return cnf

def generateRandomInterFormula(community_id_upper_bounds, cvr, k, cnf, inter_vars):
	# Select inter-community variables
	degree = len(community_id_upper_bounds) - 1
	inter_vars_per_community = [
		random.sample(
			range(community_id_upper_bounds[i] + 1, community_id_upper_bounds[i + 1] + 1),
			inter_vars / degree
		) for i in range(degree)
	]

	# Phase 1: make sure every inter-community variable appears in some clause
	for com in inter_vars_per_community:
		for iv in com:
			cnf.append(select_inter_vars(
				cnf, [var_to_lit(iv)], inter_vars_per_community, k, community_id_upper_bounds
			))

	# Phase 2: distribute the remaining clauses randomly amongst the intercommunity variables
	for c in range(int(inter_vars * cvr) - sum(len(com) for com in inter_vars_per_community)):
		cnf.append(select_inter_vars(cnf, [], inter_vars_per_community, k, community_id_upper_bounds))

	return cnf

if __name__ == "__main__":
	n = int(sys.argv[1])
	m = int(sys.argv[2])
	k = int(sys.argv[3])
