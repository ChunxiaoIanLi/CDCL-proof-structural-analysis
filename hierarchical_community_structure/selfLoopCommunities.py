import igraph
import math
import sys
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import os
import numpy as np
from random import randrange

def computeCommunityStructure(g, weight_list):
	vertex_clustering = None
	if weight_list is None:
		vertex_clustering = g.community_multilevel()
	else:
		vertex_clustering = g.community_multilevel('weight')

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

file = sys.argv[1]
clauses, m, n = read_file(file)
edge_set = cnf_to_edge_set(clauses)
edge_list = [list(e) for e in edge_set]

##### NO LOOPS #####

# Calculate community data for graph with no loops
no_loop_g = igraph.Graph()
no_loop_g.add_vertices(n)
no_loop_g.add_edges(edge_list)
no_loop_numCommunities, no_loop_avgCommunitySize, no_loop_maxCommunitySize, no_loop_modularity = computeCommunityStructure(no_loop_g, None)

##### WEIGHTED LOOPS #####

# Add weights for normal edges
weight_list = []
for e in edge_list:
	weight_list.append(1)

# Add weighted self-loops
weight = math.sqrt(n / math.log(n))
for i in range(n):
	edge_list.append([i, i])
	weight_list.append(weight)

# Calculate community data for graph with weighted loops
weighted_g = igraph.Graph()
weighted_g.add_vertices(n)
weighted_g.add_edges(edge_list)
weighted_g.es['weight'] = weight_list
weighted_numCommunities, weighted_avgCommunitySize, weighted_maxCommunitySize, weighted_modularity = computeCommunityStructure(weighted_g, 'weight')

# Output community data
modularity_f = open(file + ".loop_modularity", "w")
modularity_f.write("no_loop " + str(no_loop_numCommunities) + " " + str(no_loop_avgCommunitySize) + " " + str(no_loop_maxCommunitySize) + " " + str(no_loop_modularity) + "\n")
modularity_f.write("loop_weighted " + str(weighted_numCommunities) + " " + str(weighted_avgCommunitySize) + " " + str(weighted_maxCommunitySize) + " " + str(weighted_modularity) + "\n")
modularity_f.close()