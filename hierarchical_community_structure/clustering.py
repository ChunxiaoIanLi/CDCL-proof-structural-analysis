import igraph
import sys
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import os
import numpy as np
from random import randrange
import ctypes
lib = ctypes.CDLL('./libmergeability.so')

# An object for working with the C/C++ library
class PMI(object):
	def __init__(self):
		self.obj = lib.PMI_init()

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

def write_data(mergeability_data, modularity_data, file):
	mergeability_filename = file + ".mergeability"
	mergeability_f = open(mergeability_filename, "w")
	for i in mergeability_data:
		mergeability_f.write(",".join(i))
		mergeability_f.write("\n")
	mergeability_f.close()

	modularity_filename = file + ".modularity"
	modularity_f = open(modularity_filename, "w")
	for i in modularity_data:
		modularity_f.write(",".join(i))
		modularity_f.write("\n")
	modularity_f.close()
	return

def rgba(color, percent, opacity):
    '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''
    color = np.array(color)
    white = np.array([255, 0, 0])
    vector = white-color
    final_color = color + vector * percent
    rgba = 'rgba(' + str(final_color[0]) + ',' + str(final_color[1]) + ',' + str(final_color[2]) + ',' + str(opacity) + ')'
    return rgba

def create_directory(file):
	directory = os.path.dirname(file)
	filename =  os.path.basename(file)
	name = filename[:-4]
	if directory == '':
		output_directory = name + '/'
	else:
		output_directory = directory + '/' + name + '/'
	if not os.path.isdir(output_directory):
		os.mkdir(output_directory)
	return output_directory

def set_community_structure_style(g):
	layout = g.layout("large")
	visual_style = {}
	visual_style["layout"] = layout
	visual_style["bbox"] = (5000, 5000)
	visual_style["vertex_size"] = 1
	return visual_style

def set_hierarchical_tree_style_modularity(hierarchical_tree):
	layout = hierarchical_tree.layout_reingold_tilford(root=[0])
	visual_style = {}
	visual_style["layout"] = layout
	visual_style["bbox"] = (5000, 5000)
	visual_style["vertex_size"] = hierarchical_tree.vs['modularity_vertex_size']
	visual_style["vertex_color"] = hierarchical_tree.vs['modularity_color']
	return visual_style

def set_hierarchical_tree_style_mergeability(hierarchical_tree):
	layout = hierarchical_tree.layout_reingold_tilford(root=[0])
	visual_style = {}
	visual_style["layout"] = layout
	visual_style["bbox"] = (5000, 5000)
	visual_style["vertex_size"] = hierarchical_tree.vs['mergeability_vertex_size']
	visual_style["vertex_color"] = hierarchical_tree.vs['mergeability_color']
	return visual_style

def plot_community_structure(vertex_clustering, path, output_directory):

	filename = str(len(path) - 1)
	for i in range(len(path)):
		filename+="_"
		filename+=str(path[i])
	filename = filename + ".svg"

	igraph.plot(vertex_clustering, output_directory + filename, mark_groups = True, **community_structure_style)
	return

def plot_hierarchical_tree(hierarchical_tree, file):
	filename = file + "_modularity.svg"
	hierarchical_tree_style = set_hierarchical_tree_style_modularity(hierarchical_tree)
	igraph.plot(hierarchical_tree, filename, **hierarchical_tree_style)
	
	filename = file + "_mergeability.svg"
	hierarchical_tree_style = set_hierarchical_tree_style_mergeability(hierarchical_tree)
	igraph.plot(hierarchical_tree, filename, **hierarchical_tree_style)
	return

def create_edge_list_hierarchical_tree(current_node, number_of_children, max_node):
	edge_list = []
	for i in range(number_of_children):
		edge_list.append([current_node, max_node-i])
	return edge_list

def compute_hierarchical_community_structure(g, hierarchical_tree, current_node, path, pmi, mergeability_data, modularity_data):
	#calculates community structure
	vertex_clustering = g.community_multilevel()
	#vertex_clustering = g.community_edge_betweenness().as_clustering()
	#plot all sub-communities and saving them to files.
	#plot_community_structure(vertex_clustering, path, output_directory)

	#color the node using its modularity
	percent = (g.modularity(vertex_clustering) + 0.5) / 1.5
	hierarchical_tree.vs[current_node]['modularity_color'] = rgba((255, 245, 245), percent, 0.8)
	hierarchical_tree.vs[current_node]['modularity_vertex_size'] = 200*percent

	#color the node using its mergeability
	vertices= []
	for v in g.vs():
		vertices.append(int(v['name']) + 1)
	vertices.append(0)
	pmi.calculateMergeability(vertices)
	percent = pmi.getMergeabilityScoreNorm1() / 0.5
	hierarchical_tree.vs[current_node]['mergeability_color'] = rgba((255, 245, 245), percent, 0.8)
	hierarchical_tree.vs[current_node]['mergeability_vertex_size'] = 2000*percent

	if len(path) > len(mergeability_data):
		mergeability_data.append([])
		modularity_data.append([])
	mergeability_data[len(path)-1].append(str(pmi.getMergeabilityScoreNorm1()))
	modularity_data[len(path)-1].append(str(g.modularity(vertex_clustering)))

	if len(vertex_clustering) > 1:
		#modifying hierarchical community structure tree
		hierarchical_tree.add_vertices(len(vertex_clustering))
		hierarchical_tree.add_edges(create_edge_list_hierarchical_tree(current_node, len(vertex_clustering), hierarchical_tree.vcount()-1))
		current_max_node = hierarchical_tree.vcount()-1

		for c in range(len(vertex_clustering)):
			current_node = current_max_node - c
			temp_path = path[:]
			temp_path.append(c)
			compute_hierarchical_community_structure(vertex_clustering.subgraph(c), hierarchical_tree, current_node, temp_path, pmi, mergeability_data, modularity_data)
	return

file = sys.argv[1]
print(file)

# Configure ctypes to work with library functions
lib.PMI_setClauses.restype = None
lib.PMI_calculateMergeability.restype = None
lib.PMI_getMergeabilityScoreNorm1.restype = ctypes.c_double
lib.PMI_getMergeabilityScoreNorm2.restype = ctypes.c_double
# Create object
pmi = PMI()

#output_directory = create_directory(file)
clauses, m, n = read_file(file)
edge_set = cnf_to_edge_set(clauses)
edge_list = [list(e) for e in edge_set]
clauses_list = cnf_to_clauses_list(clauses)

# Load the clauses
pmi.setClauses(clauses_list)

g = igraph.Graph()
g.add_vertices(n)
g.add_edges(edge_list)
for i in range(n):
	g.vs[i]['name'] = i
path = [0]

hierarchical_tree = igraph.Graph()
hierarchical_tree.add_vertices(1)
current_node = 0

mergeability_data=[]
modularity_data=[]

#community_structure_style = set_community_structure_style(g)

#compute_hierarchical_community_structure(g, hierarchical_tree, current_node, path, output_directory)
compute_hierarchical_community_structure(g, hierarchical_tree, current_node, path, pmi, mergeability_data, modularity_data)
plot_hierarchical_tree(hierarchical_tree, file)
write_data(mergeability_data, modularity_data, file)
