import igraph
import math
import sys
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import os
import numpy as np
from random import randrange

def addWeightedLoops(edge_list, weight_list, n, weight):
	for i in range(n):
		edge_list.append([i, i])
		weight_list.append(weight)

def computeCommunityStructure(g):
	vertex_clustering = g.community_multilevel()
	totalCommunitySize = 0
	maxCommunitySize = 0
	numCommunities = len(vertex_clustering)
	for community in vertex_clustering:
		communitySize = len(community)
		totalCommunitySize += communitySize
		maxCommunitySize = max(maxCommunitySize, communitySize)
	avgCommunitySize = totalCommunitySize / float(numCommunities)
	modularity = g.modularity(vertex_clustering)
	return numCommunities, avgCommunitySize, maxCommunitySize, modularity

def write_data(file, numCommunities, avgCommunitySize, maxCommunitySize, modularity):
	modularity_filename = file + ".loop_modularity"
	modularity_f = open(modularity_filename, "w")
	modularity_f.write(str(numCommunities) + "," + str(avgCommunitySize) + "," + str(maxCommunitySize) + "," + str(modularity) + "\n")
	modularity_f.close()

file = sys.argv[1]
clauses, m, n = read_file(file)
edge_set = cnf_to_edge_set(clauses)
edge_list = [list(e) for e in edge_set]
weight_list = []
clauses_list = cnf_to_clauses_list(clauses)

# Add weights for normal edges
for e in edge_list:
	weight_list.append(1)

# Add weighted self-loops
weight = math.sqrt(n / math.log(n))
addWeightedLoops(edge_list, weight_list, n, weight)

g = igraph.Graph()
g.add_vertices(n)
g.add_edges(edge_list)

numCommunities, avgCommunitySize, maxCommunitySize, modularity = computeCommunityStructure(g)
write_data(file, numCommunities, avgCommunitySize, maxCommunitySize, modularity)
