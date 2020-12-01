import igraph
import sys
import os
import random
import math

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

def pick_k_lits(dv, k):
	cummulative_vec = generateCummulative(dv)
	k_lits = []
	v_sum = vecsum(dv)
	for i in range(k):
		r = random.randint(0, v_sum)
		for v in range(len(cummulative_vec)):
			if r <= cummulative_vec[v]:
				polarity=random.randint(0,1)
				if polarity == 0:
					k_lits.append(-1*(v+1))
				else:
					k_lits.append(v+1)
				break
	return k_lits

def is_clique(g, k_lits):
	vertices = []
	#TODO this is assuming vertex 0 corresponds to variable 1, etc
	for i in k_lits:
		vertices.append(abs(i)-1)

	subgraph = g.subgraph(vertices)
	if subgraph.ecount() == (subgraph.vcount()*(subgraph.vcount()-1)/2):
		return True
	return False

def mark_visited(g, k_lits):
	for i in k_lits:
		g.vs[abs(i)-1]['visited'] = True
	return

def all_edges_visited(g):
	for i in range(g.vcount()):
		if g.vs[i]['visited'] == False:
			return False
	return True

def print_cnf(cnf, n, m):
	print("p cnf {0} {1}".format(n, m))
	for c in cnf:
		outstr = ""
		for l in c:
			outstr+=str(l)
			outstr+=" "
		outstr+="0"
		print(outstr)
	return

def reset_visited_flag(g):
	for i in range(g.vcount()):
		g.vs[i]['visited'] = False
	return

# g: VIG
# m: number of clauses to generate
# k: k-sat
def VIG_to_CNF(g, m, k):
	# degree_distribution can be powerlaw, with a specific beta, or a balanced one
	# where variable occurrences are uniform
	# degree_distribution is a vector of integers
	dv = generateUniformVec(g.vcount(), m, k)

	trial = 1
	while True:
		print(trial)
		# cnf is a vector of clauses, a clause is a vector of integers
		cnf = []
		# TODO: assignVarsToDegreeDistribution()
		for i in range(m):
			# Step 1: adding the new clause to the formula
			while True:
				# TODO: are we allowing to generate clauses with width less than k
				k_lits = pick_k_lits(dv, k)
				if is_clique(g, k_lits):
					break
			cnf.append(k_lits)
			# Step 2: label the edges corresponding to the added clause as "visited"
			mark_visited(g, k_lits)

		# TODO: we do this check if missing few edges in the VIG doesn't change the HCS too much
		if all_edges_visited(g):
			return cnf
		reset_visited_flag(g)
		trial+=1


m = int(sys.argv[1])
k = int(sys.argv[2])
p = float(sys.argv[3])

g = igraph.Graph.Erdos_Renyi(300, p)
n = g.vcount()
for i in range(n):
	g.vs[i]['name'] = i
	g.vs[i]['visited'] = False

layout = g.layout("large")
visual_style = {}
visual_style["vertex_size"] = 5
visual_style["vertex_label"] = g.vs["name"]
visual_style["layout"] = layout
visual_style["bbox"] = (1000, 1000)
visual_style["margin"] = 10

igraph.plot(g, "randomgraph_200_0.6.svg", **visual_style)




cnf = VIG_to_CNF(g, m, k)
print_cnf(cnf, n, m)



# check whether ps-generator has a powerlaw tail cutoff

# ranges for beta:  above (k-1)/k whp has a contradiction on constantly many heavy-hitters.
# for lower bounds, I think beta <1/2 for exponential,  beta < 3/4 - 1/(2k)

#want to choose 1/2 < beta < (k-1)/k



