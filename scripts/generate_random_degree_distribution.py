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

def get_k_lits(tmp_clause, m, k, cumulative_vec):
	for l in range(k):
		found = False
		while not found:
			r = random.randint(0, m * k)
			for i in range(len(cumulative_vec)):
				if r <= cumulative_vec[i]:
					if (i + 1 not in tmp_clause) and (-i - 1 not in tmp_clause):
						tmp_clause.append(i + 1)
						found = True
						if random.randint(0, 1): tmp_clause[-1] *= -1
						break
	tmp_clause.sort()
	return tmp_clause

def get_new_clause(cnf, clause, m, k, cumulative_vec):
	tmp_clause = get_k_lits(clause[:], m, k, cumulative_vec)
	while tmp_clause in cnf:
		tmp_clause = get_k_lits(clause[:], m, k, cumulative_vec)
	cnf.append(tmp_clause)
	return

def var_to_lit(var):
	return var if random.randint(0, 1) else var * -1

def same_community(u, v, community_id_upper_bounds):
    previous = 0
    for current in community_id_upper_bounds:
        if previous <= u < current and previous <= v < current:
            return True
        previous = current
    return False

def all_same_community(lits, community_id_upper_bounds):
    result = True
    for i in range(len(lits)):
        for j in range(i+1, len(lits)):
            if not same_community(abs(lits[i]), abs(lits[j]), community_id_upper_bounds):
                return False
    return result

def select_inter_vars(cnf, clause, inter_vars_per_community, k, community_id_upper_bounds):
    while True:
        temp_clause = clause[:]
        for l in range(k):
            random_comm = random.randint(0, len(inter_vars_per_community)-1)
            random_var = random.sample(inter_vars_per_community[random_comm], 1)[0]
            if random_var == 0  :
                print(random_var)
            temp_clause.append(var_to_lit(random_var))

        temp_clause.sort()
        if not all_same_community(temp_clause, community_id_upper_bounds):
            if temp_clause not in cnf:
                return temp_clause


def generateRandomFormula(n, m, k, cummulative_vec):
    cnf = []
    clauses = 0
    # phase 1: make sure every variable is covered
    for variable_id in range(n):
        clause = [variable_id+1]
        get_new_clause(cnf, clause, m, k-1, cummulative_vec)

    for clause_id in range(m-n):
        clause = []
        get_new_clause(cnf, clause, m, k, cummulative_vec)
    return cnf

def generateRandomInterFormula(community_id_upper_bounds, cvr, k, cnf, inter_vars):
    degree = len(community_id_upper_bounds) - 1

    inter_vars_per_community = []
    actual_inter_vars = 0

    for i in range(0, degree):
        actual_inter_vars += inter_vars/degree
        random_vars = random.sample(range(community_id_upper_bounds[i]+1, community_id_upper_bounds[i+1]+1), inter_vars/degree)
        inter_vars_per_community.append(random_vars)

    actual_inter_cls = int(actual_inter_vars * cvr)

    inter_clause_count = 0
    #phase 1: makes sure every inter_var appears in some clause
    for com_id, com in enumerate(inter_vars_per_community):
        for iv in com:
            temp_clause = [var_to_lit(iv)]
            temp_clause = select_inter_vars(cnf, temp_clause, inter_vars_per_community, k-1, community_id_upper_bounds)
            cnf.append(temp_clause)
            inter_clause_count += 1

    #phase 2: distribute the remaining clauses randomly
    for c in range(actual_inter_cls - inter_clause_count):
        temp_clause = []
        temp_clause = select_inter_vars(cnf, temp_clause, inter_vars_per_community, k, community_id_upper_bounds)
        cnf.append(temp_clause)

    return cnf

if __name__ == "__main__":
    n=int(sys.argv[1])
    m=int(sys.argv[2])
    k=int(sys.argv[3])

# #generating uniform
# uniformvec=generateUniformVec(n, m, k)
# cummulative_vec=generateCummulative(uniformvec)
# for i in range(200):
#     outf=open("instances/uniform/{0}.cnf".format(i),"w")
#     outf.write("p cnf {0} {1}\n".format(n, m))
#     generateRandomFormula(n, m, k, cummulative_vec, outf)
#     outf.close()

# # #generating powerlaw
# powerlawvec=generatePowerlawVec(n, m, k)
# cummulative_vec=generateCummulative(powerlawvec)
# for i in range(200):
#     outf=open("instances/powerlaw/{0}.cnf".format(i),"w")
#     outf.write("p cnf {0} {1}\n".format(n, m))
#     generateRandomFormula(n, m, k, cummulative_vec, outf)
#     outf.close()

# # #generating medium
# for i in range(200):
#     mediumvec=generateMediumVec(n, m, k)
#     cummulative_vec=generateCummulative(mediumvec)
#     outf=open("instances/medium/{0}.cnf".format(i),"w")
#     outf.write("p cnf {0} {1}\n".format(n, m))
#     generateRandomFormula(n, m, k, cummulative_vec, outf)
#     outf.close()



