import sys
import math
import os
import random

# generates a uniform degree vector with n variables, m clauses and width k
def generateUniformVec(n, m, k):
    ave = int(m*k/n)
    remainder= int((m*k)%n)
    vec = [ave]*n
    while remainder > 0:
        vec[remainder-1]+=1
        remainder-=1
    return vec

# generates a powerlaw degree vector with n variables, m clauses and width k
def generatePowerlawVec(n, m, k):
    vec=generateUniformVec(int(n/2), m, k)
    
    for i in range(len(vec)):
        vec[i]-=1
        vec.append(1)

    if n%2 == 1:
        vec[(m*k)%(n/2)-1]-=1
        vec.append(1)
    return vec

# generates a degree vector with n variables, m clauses and width k that is not too balanced and
# also not too unblanced
def generateMediumVec(n, m, k):
    #somehow vec[0] is not modified after this call?
    vec=generatePowerlawVec(n, m, k)
    max=vec[0]-2
    for i in range(n/2):
        diff=random.randint(0, max)
        vec[i]-=diff
        vec[-i]+=diff
    return vec

# input:
#   vec                     :   a degree vector [a, b, c, d, ...]
# output:
#   cummulative_vec         :   [a, a+b, a+b+c, a+b+c+d, ...]
def generateCummulative(vec):
    cummulative_vec=[vec[0]]
    for i in vec[1:]:
        cummulative_vec.append(i + cummulative_vec[-1])
    return cummulative_vec


def clause_existing(cnf, clause):
    if clause in cnf:
        return True
    return False


# assigns the polarity of var randomly
def var_to_lit(var):
    polarity=random.randint(0,1)
    if polarity == 0:
        return var*-1
    return var

# input:
#   u                           :   a variable
#   v                           :   a variable
#   community_id_upper_bounds   :   an array of non-negative integers [0, x, y, z, ...] where x is the
#                                   size of community 1, y-x is the size of community 2, and z-x is the
#                                   size of community 3
# output:
#   result                      :   True if all the literals in liters are from the same community,
#                                   False otherwise
def same_community(u, v, community_id_upper_bounds):
    previous = 0
    for current in community_id_upper_bounds:
        if previous <= u < current and previous <= v < current:
            return True
        previous = current
    return False

# input:
#   lits                        :   a vector of literals
#   community_id_upper_bounds   :   an array of non-negative integers [0, x, y, z, ...] where x is the
#                                   size of community 1, y-x is the size of community 2, and z-x is the
#                                   size of community 3
# output:
#   result                      :   True if all the literals in liters are from the same community,
#                                   False otherwise
def all_same_community(lits, community_id_upper_bounds):
    result = True
    for i in range(len(lits)):
        for j in range(i+1, len(lits)):
            if not same_community(abs(lits[i]), abs(lits[j]), community_id_upper_bounds):
                return False
    return result

# input:
#   temp_clause             :   an array that either conains zero or one integer
#   k                       :   clause width
#   cumulative_vec          :   the cummulative_vec of degree vector [a, b, c, d, ...] 
#                               is [a, a+b, a+b+c, a+b+c+d, ...]
# output:
#   temp_clause             :   an intra-community clause of width k
def get_k_lits(temp_clause, k, cummulative_vec):
    for l in range(k):
        found = False
        while not found:
            r = random.randint(0, cummulative_vec[-1])
            for i in range(len(cummulative_vec)):
                if r <= cummulative_vec[i]:
                    if i+1 not in temp_clause:
                        temp_clause.append(i+1)
                        found = True
                        polarity=random.randint(0,1)
                        if polarity == 0:
                            temp_clause[-1] *= -1
                        break;
    temp_clause.sort()
    return temp_clause


# input:
#   cnf                         :   A 2D array of clauses
#   clause                      :   an array that either conains zero or one integer
#   k                           :   clause width
#   cumulative_vec              :   the cummulative_vec of degree vector [a, b, c, d, ...] 
#                                   is [a, a+b, a+b+c, a+b+c+d, ...]
# output:
#   cnf                         :   the input cnf with one more clause

def get_new_clause(cnf, clause, k, cummulative_vec):
    tmp_clause = get_k_lits(clause, k, cummulative_vec)
    while clause_existing(cnf, tmp_clause) is True:
        tmp_clause = get_k_lits(clause, k, cummulative_vec)
    cnf.append(tmp_clause)
    return

# fill clause with k random chosen literals
# reroll if all literals are from the same community
# input:
#   cnf                         :   A 2D array of clauses
#   clause                      :   an array that either conains zero or one integer
#   inter_vars_per_community    :   A 2D array where the i'th element is an array containing the
#                                   inter-community variables from the i'th community
#   k                           :   clause width
#   community_id_upper_bounds   :   an array of non-negative integers [0, x, y, z, ...] where x is the
#                                   size of community 1, y-x is the size of community 2, and z-x is the
#                                   size of community 3
# output:
#   temp_clause                 :   an inter-community clause of width k
def select_inter_vars(cnf, clause, inter_vars_per_community, k, community_id_upper_bounds):
    while True:
        temp_clause = clause[:]
        for l in range(k):
            random_comm = random.randint(0, len(inter_vars_per_community)-1)
            random_var = random.sample(inter_vars_per_community[random_comm], 1)[0]
            temp_clause.append(var_to_lit(random_var))

        temp_clause.sort()
        if not all_same_community(temp_clause, community_id_upper_bounds):
            if not clause_existing(cnf, temp_clause):
                return temp_clause

# this function is for generating leaf community clauses, it basically
# generates a random k-cnf of n variables and m clauses whose degree distribution
# is described by cummulative_vec
def generateRandomFormula(n, m, k, cummulative_vec):
    cnf = []
    clauses = 0
    # phase 1: make sure every variable is covered
    for variable_id in range(n):
        # makes sure the variable we want to cover is in the clause
        clause = [variable_id+1]
        # fill the clause with k-1 other literals randomly chosen according to a degree distribution
        # and add that clause to cnf
        get_new_clause(cnf, clause, k-1, cummulative_vec)

    # phase 2: generate the remaining clauses
    for clause_id in range(m-n):
        clause = []
        # fill the clause with k literals randomly chosen according to a degree distribution
        # and add that clause to cnf
        get_new_clause(cnf, clause, k, cummulative_vec)
    return cnf

# this function is for generating inter-community clauses
# input:
#   community_id_upper_bounds   :   an array of non-negative integers [0, x, y, z, ...] where x is the
#                                   size of community 1, y-x is the size of community 2, and z-x is the
#                                   size of community 3 
#   cvr                         :   clause variable ratio
#   k                           :   clause width
#   cnf                         :   all the clauses we have so far
#   inter_vars                  :   total number of inter_community variables
# output:
#   cmf                         :   contains intra-community clauses and inter-community clauses
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
            # makes sure the variable we want to cover is in the clause
            temp_clause = [var_to_lit(iv)]
            # fill the clause with k-1 random chosen literals
            # reroll if all literals are from the same community
            temp_clause = select_inter_vars(cnf, temp_clause, inter_vars_per_community, k-1, community_id_upper_bounds)
            cnf.append(temp_clause)
            inter_clause_count += 1

    #phase 2: distribute the remaining clauses randomly
    for c in range(actual_inter_cls - inter_clause_count):
        temp_clause = []
        # fill the clause with k random chosen literals
        # reroll if all literals are from the same community
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



