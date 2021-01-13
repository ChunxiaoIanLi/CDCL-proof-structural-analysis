import igraph
import sys
import os
import random
import math
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list

def generateUniformVec(n, m, k):
	ave = int(m*k/n)
	remainder= int((m*k)%n)
	vec = [ave]*n
	while remainder > 0:
		vec[remainder-1]+=1
		remainder-=1
	return vec

def generatePowerlawVec(n, m, k):
	vec = []
	return vec

def generateCummulative(vec):
	cummulative_vec=[vec[0]]
	for i in vec[1:]:
		cummulative_vec.append(i + cummulative_vec[-1])
	return cummulative_vec

def vecsum(vec):
	sum = 0
	for i in vec:
		sum+=i
	return sum

def initialize_graph(g):
	n = g.vcount()
	for i in range(n):
		g.vs[i]['name'] = i
	for e in g.es:
		e["visited"] = False
	return g

def var_to_lit(v):
	polarity=random.randint(0,1)
	if polarity == 0:
		return -1*(v+1)
	else:
		return v+1

def pick_k_lits(dv, k):
	# TODO: random.choices()
	cummulative_vec = generateCummulative(dv)
	k_lits = []
	v_sum = vecsum(dv)
	for i in range(k):
		r = random.randint(0, v_sum - 1)
		# TODO: binary search or search for python functions that do this
		for v in range(len(cummulative_vec)):
			if r < cummulative_vec[v]:
				k_lits.append(var_to_lit(v))
				break
	return k_lits

def is_clique(g, k_lits):
	vertices = []
	#TODO this is assuming vertex 0 corresponds to variable 1, etc
	for i in k_lits:
		if not abs(i)-1 in vertices:
			vertices.append(abs(i)-1)

	# TODO: perhaps use g.es.select(_within=vertices) and check the number of edges
	subgraph = g.subgraph(vertices)
	return subgraph.ecount() == (subgraph.vcount()*(subgraph.vcount()-1)/2)

def mark_visited(g, k_lits):
	vertices = []
	for i in k_lits:
		vertices.append(abs(i)-1)
	edges_in_clique = g.es.select(_within=vertices)
	for i in edges_in_clique:
		i['visited'] = True
	return

def all_edges_visited(g):
	for e in g.es:
		if e["visited"] == False:
			return False
	return True

def count_unvisited(g):
	counter = 0
	for e in g.es:
		if e["visited"] == False:
			counter+=1
	return counter

def print_cnf(cnf, n):
	m = len(cnf)
	print("p cnf {0} {1}".format(n, m)) 
	for c in cnf:
		outstr = ""
		for l in c:
			outstr+=str(l)
			outstr+=" "
		outstr+="0"
		print(outstr)
	return

def write_cnf(cnf, n, file):
	m = len(cnf)
	fp = open(file, "w")
	fp.write("p cnf {0} {1}\n".format(n, m))
	for c in cnf:
		outstr = ""
		for l in c:
			outstr+=str(l)
			outstr+=" "
		outstr+="0\n"
		fp.write(outstr)
	return

def reset_visited_flag(g):
	for e in g.es:
		e["visited"] = False
	return

def compute_phase_one_clauses(g, k):
	clauses = []
	for e in g.es:
		if e["visited"] == False:
			clause = []
			u = e.source
			v = e.target
			# try to find a k-clique
			u_neighbors = g.neighbors(u)
			v_neighbors = g.neighbors(v)
			common_vertices = list(set(u_neighbors).intersection(v_neighbors))
			vertices_in_clique = []
			vertices_in_clique.append(u)
			vertices_in_clique.append(v)

			clause.append(var_to_lit(u))
			clause.append(var_to_lit(v))
			if len(common_vertices) >= k - 2:
				w = random.sample(common_vertices, 1)[0]
				vertices_in_clique.append(w)
				clause.append(var_to_lit(w))

			edges_in_clique = g.es.select(_within=vertices_in_clique)
			for i in edges_in_clique:
				i['visited'] = True

			clauses.append(clause)
	return clauses

def compute_phase_two_clauses(g, k, m):
	clauses = []
	for i in range(m):
		e = random.sample(g.es, 1)[0]
		#print(g.es)
		clause = []
		u = e.source
		v = e.target
		# try to find a k-clique
		u_neighbors = g.neighbors(u)
		v_neighbors = g.neighbors(v)
		common_vertices = list(set(u_neighbors).intersection(v_neighbors))
		vertices_in_clique = []
		vertices_in_clique.append(u)
		vertices_in_clique.append(v)

		clause.append(var_to_lit(u))
		clause.append(var_to_lit(v))
		if len(common_vertices) >= k - 2:
			w = random.sample(common_vertices, 1)[0]
			vertices_in_clique.append(w)
			clause.append(var_to_lit(w))
		clauses.append(clause)	
	return clauses

def count_binary_ternary(clauses):
	binary_counter = 0
	ternary_counter = 0
	for c in clauses:
		if len(c) == 2:
			binary_counter+=1
		if len(c) == 3:
			ternary_counter+=1
	print("binary {0}".format(binary_counter))
	print("ternary {0}".format(ternary_counter))
	return

# g: VIG
# m: number of clauses to generate
# k: k-sat
def VIG_to_CNF(g, m, k):
	# degree_distribution can be powerlaw, with a specific beta, or a balanced one
	# where variable occurrences are uniform
	# degree_distribution is a vector of integers
	dv = generateUniformVec(g.vcount(), m, k)
	initialize_graph(g)

	# cnf is a vector of clauses, a clause is a vector of integers
	cnf = []
	# TODO: assignVarsToDegreeDistribution()
	# Phase 1: generate clauses such that every edge appears in some clauses
	printed=False
	while True:
		phase_one_clauses = compute_phase_one_clauses(g, k)
		count_binary_ternary(phase_one_clauses)
		# add an early exist if len(phase_one_clauses) - m << 0, proportion to m
		if not printed:
			print("Phase 1: used {0}/{1} clauses to cover all edges.".format(len(phase_one_clauses), m))
			printed = True
		if len(phase_one_clauses) <= m:
			cnf = phase_one_clauses
			break
		else:
			reset_visited_flag(g)
	# Phase 2: assigning remaining edges
	print("Phase 2: generating remaining clauses.")
	phase_two_clauses = compute_phase_two_clauses(g, k, m - len(phase_one_clauses))
	count_binary_ternary(phase_two_clauses)
	cnf += phase_two_clauses
	return cnf

# file = str(sys.argv[1])
# # n is the number of variables
# # n = int(sys.argv[1])
# # m is the number of clauses to generate
# m = int(sys.argv[2])
# # k is the width of clauses
# k = int(sys.argv[3])
# #p = float(sys.argv[4])

# clauses, temp, n = read_file(file)
# edge_set = cnf_to_edge_set(clauses)
# edge_list = [list(e) for e in edge_set]
# g = igraph.Graph()
# g.add_vertices(n)
# g.add_edges(edge_list)

# #g = igraph.Graph.Erdos_Renyi(n, p)
# n = g.vcount()
# for i in range(n):
# 	g.vs[i]['name'] = i
# 	#g.vs[i]['visited'] = False
# 	for e in g.es:
# 		e["visited"] = False

# cnf = VIG_to_CNF(g, m, k)
# print_cnf(cnf, n, m)



# check whether ps-generator has a powerlaw tail cutoff

# ranges for beta:  above (k-1)/k whp has a contradiction on constantly many heavy-hitters.
# for lower bounds, I think beta <1/2 for exponential,  beta < 3/4 - 1/(2k)

#want to choose 1/2 < beta < (k-1)/k



