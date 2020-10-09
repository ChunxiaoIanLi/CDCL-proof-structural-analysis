import igraph
import sys
from cnf_to_edge_set import cnf_to_edge_set, read_file, cnf_to_clauses_list
import os
import numpy as np
from random import randrange
import ctypes
lib = ctypes.CDLL('/home/ianli/CDCL-proof-structural-analysis/scripts/resolvability/libmergeability.so')

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

	degree_filename = file + ".degree"
	degree_f = open(degree_filename, "w")
	for i in degree_data:
		degree_f.write(",".join(i))
		degree_f.write("\n")
	degree_f.close()

	community_size_filename = file + ".community_size"
	community_size_f = open(community_size_filename, "w")
	for i in community_size_data:
		community_size_f.write(",".join(i))
		community_size_f.write("\n")
	community_size_f.close()

	inter_edges_filename = file + ".inter_edges"
	inter_edges_f = open(inter_edges_filename, "w")
	for i in inter_edges_data:
		inter_edges_f.write(",".join(i))
		inter_edges_f.write("\n")
	inter_edges_f.close()

	inter_vars_filename = file + ".inter_vars"
	inter_vars_f = open(inter_vars_filename, "w")
	for i in inter_vars_data:
		inter_vars_f.write(",".join(i))
		inter_vars_f.write("\n")
	inter_vars_f.close()

	pre_width_filename = file + ".pre_width"
	pre_width_f = open(pre_width_filename, "w")
	for i in pre_width_data:
		pre_width_f.write(",".join(i))
		pre_width_f.write("\n")
	pre_width_f.close()

	post_width_filename = file + ".post_width"
	post_width_f = open(post_width_filename, "w")
	for i in post_width_data:
		post_width_f.write(",".join(i))
		post_width_f.write("\n")
	post_width_f.close()
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

def computer_intercommunity_edges(vertex_clustering):
	crossing = vertex_clustering.crossing()
	num_inter_edges = 0
	for i in crossing:
		if i == True:
			num_inter_edges += 1
	return num_inter_edges

def computer_intercommunity_vars(g, vertex_clustering):
	crossing = vertex_clustering.crossing()
	var_occurrence = [0]*g.vcount()
	es = g.es()

	for i in range(len(crossing)):
		if crossing[i] == True:
			v1 = es[i].tuple[0]
			v2 = es[i].tuple[1]
			var_occurrence[v1] |= 1

	return var_occurrence.count(1)

def compute_hierarchical_community_structure(g, hierarchical_tree, current_node, path, pmi, mergeability_data, modularity_data, degree_data, community_size_data, inter_edges_data, inter_vars_data, pre_width_data, post_width_data):
	#calculates community structure
	vertex_clustering = g.community_multilevel()

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
		degree_data.append([])
		community_size_data.append([])
		inter_edges_data.append([])
		inter_vars_data.append([])
		pre_width_data.append([])
		post_width_data.append([])
	mergeability_data[len(path)-1].append(str(pmi.getMergeabilityScoreNorm1()))
	modularity_data[len(path)-1].append(str(g.modularity(vertex_clustering)))
	degree_data[len(path)-1].append(str(len(vertex_clustering)))
	community_size_data[len(path)-1].append(str(g.vcount()))
	inter_edges_data[len(path)-1].append(str(computer_intercommunity_edges(vertex_clustering)))
	inter_vars_data[len(path)-1].append(str(computer_intercommunity_vars(g, vertex_clustering)))
	pre_width_data[len(path)-1].append(str(pmi.PMI_getPreResolutionClauseWidth()))
	post_width_data[len(path)-1].append(str(pmi.PMI_getPostResolutionClauseWidth()))

	if len(vertex_clustering) > 1:
		#modifying hierarchical community structure tree
		hierarchical_tree.add_vertices(len(vertex_clustering))
		hierarchical_tree.add_edges(create_edge_list_hierarchical_tree(current_node, len(vertex_clustering), hierarchical_tree.vcount()-1))
		current_max_node = hierarchical_tree.vcount()-1

		for c in range(len(vertex_clustering)):
			current_node = current_max_node - c
			temp_path = path[:]
			temp_path.append(c)
			compute_hierarchical_community_structure(vertex_clustering.subgraph(c), hierarchical_tree, current_node, temp_path, pmi, mergeability_data, modularity_data, degree_data, community_size_data, inter_edges_data, inter_vars_data, pre_width_data, post_width_data)
	return

file = sys.argv[1]
print(file)

# Configure ctypes to work with library functions
lib.PMI_setClauses.restype = None
lib.PMI_calculateMergeability.restype = None
lib.PMI_getMergeabilityScoreNorm1.restype = ctypes.c_double
lib.PMI_getMergeabilityScoreNorm2.restype = ctypes.c_double
lib.PMI_getPreResolutionClauseWidth.restype = ctypes.c_double
lib.PMI_getPostResolutionClauseWidth.restype = ctypes.c_double
# Create object
pmi = PMI()


output_directory = create_directory(file)
clauses, m, n = read_file(file)
print("n: {0}".format(n))
print("m: {0}".format(m))
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
degree_data=[]
community_size_data=[]
inter_edges_data=[]
inter_vars_data=[]
pre_width_data=[]
post_width_data=[]


#community_structure_style = set_community_structure_style(g)

#compute_hierarchical_community_structure(g, hierarchical_tree, current_node, path, output_directory)
compute_hierarchical_community_structure(g, hierarchical_tree, current_node, path, pmi, mergeability_data, modularity_data, degree_data, community_size_data, inter_edges_data, inter_vars_data, pre_width_data, post_width_data)
plot_hierarchical_tree(hierarchical_tree, file)
write_data(mergeability_data, modularity_data, file)
