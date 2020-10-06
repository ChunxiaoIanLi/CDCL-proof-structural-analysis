import igraph
import sys
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import os
import numpy as np
from random import randrange

def computeCommunityStructure(g):
	vertex_clustering = g.community_multilevel()
	totalCommunitySize = 0
	maxCommunitySize = 0
	numCommunities = len(vertex_clustering)
	for community in vertex_clustering:
		totalCommunitySize += len(community)
		maxCommunitySize = max(maxCommunitySize, len(community))
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
clauses_list = cnf_to_clauses_list(clauses)

# Add self-loops
for i in range(n):
	edge_list.append([i, i])

g = igraph.Graph()
g.add_vertices(n)
g.add_edges(edge_list)
for i in range(n):
	g.vs[i]['name'] = i

numCommunities, avgCommunitySize, maxCommunitySize, modularity = computeCommunityStructure(g)
write_data(file, numCommunities, avgCommunitySize, maxCommunitySize, modularity)
