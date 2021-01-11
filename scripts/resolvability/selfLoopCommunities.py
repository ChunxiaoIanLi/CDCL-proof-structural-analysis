import igraph
import math
import sys
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import os
import numpy as np
from random import randrange

# Use ctypes to call our C/C++ code
import ctypes
lib = ctypes.CDLL('./libmergeability.so')

# An object for working with the C/C++ library
class PMI(object):
	def __init__(self):
		self.obj = lib.PMI_init()

		# Configure ctypes to work with library functions
		lib.PMI_setClauses.restype = None
		lib.PMI_calculateMergeability.restype = None
		lib.PMI_getMergeabilityScoreNorm1.restype = ctypes.c_double
		lib.PMI_getMergeabilityScoreNorm2.restype = ctypes.c_double
		lib.PMI_getPreResolutionClauseWidth.restype = ctypes.c_double
		lib.PMI_getPostResolutionClauseWidth.restype = ctypes.c_double

	def setClauses(self, clauses):
		arr = (ctypes.c_longlong * len(clauses))(*clauses)
		lib.PMI_setClauses.argtypes = [ ctypes.c_void_p, ctypes.c_longlong * len(clauses), ctypes.c_longlong ]
		lib.PMI_setClauses(self.obj, arr, len(clauses))

	def calculateMergeability(self, varSet):
		arr = (ctypes.c_longlong * len(varSet))(*varSet)
		lib.PMI_calculateMergeability.argtypes = [ ctypes.c_void_p, ctypes.c_longlong * len(varSet) ]
		lib.PMI_calculateMergeability(self.obj, arr)

	# Normalize mergeability score by total number of resolvable pairs
	def getMergeabilityScoreNorm1(self):
		lib.PMI_getMergeabilityScoreNorm1.argtypes = [ ctypes.c_void_p ]
		return lib.PMI_getMergeabilityScoreNorm1(self.obj)

	# Normalize mergeability score by m^2
	def getMergeabilityScoreNorm2(self):
		lib.PMI_getMergeabilityScoreNorm2.argtypes = [ ctypes.c_void_p ]
		return lib.PMI_getMergeabilityScoreNorm2(self.obj)

	# Get the average clause width before resolution
	def getPreResolutionClauseWidth(self):
		lib.PMI_getPreResolutionClauseWidth.argtypes = [ ctypes.c_void_p ]
		return lib.PMI_getPreResolutionClauseWidth(self.obj)

	# Get the average clause width of clauses generated by the first step of resolution
	def getPostResolutionClauseWidth(self):
		lib.PMI_getPostResolutionClauseWidth.argtypes = [ ctypes.c_void_p ]
		return lib.PMI_getPostResolutionClauseWidth(self.obj)

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
	modularity_f.write(str(numCommunities) + " " + str(avgCommunitySize) + " " + str(maxCommunitySize) + " " + str(modularity) + "\n")
	modularity_f.close()

file = sys.argv[1]
clauses, m, n = read_file(file)
edge_set = cnf_to_edge_set(clauses)
edge_list = [list(e) for e in edge_set]
weight_list = []

# Add weights for normal edges
for e in edge_list:
	weight_list.append(1)

# Add weighted self-loops
weight = math.sqrt(n / math.log(n))
addWeightedLoops(edge_list, weight_list, n, weight)

# Add data to igraph
g = igraph.Graph()
g.add_vertices(n)
g.add_edges(edge_list)
g.es['weight'] = weight_list

# Calculate and output community data
numCommunities, avgCommunitySize, maxCommunitySize, modularity = computeCommunityStructure(g)
write_data(file, numCommunities, avgCommunitySize, maxCommunitySize, modularity)
