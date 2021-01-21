import sys
import igraph

# Define all parameters
parameters = [
	'depth'             ,
	'degree'            ,
	'community_size'    ,
	'cvr'               ,
	'inter_edges'       ,
	'inter_vars'        ,
	'mergeability1norm1',
	'mergeability1norm2',
	'mergeability2norm1',
	'mergeability2norm2',
	'modularity'        ,
	'post_width'        ,
	'pre_width'         ,
]

def reconstruct_community_edges(degrees):
	"""Reconstruct the edges of the HCS tree"""
	edges = []
	offset = 1
	for i, degree in enumerate(degrees):
		if degree == 1: continue
		for j in range(offset, offset + degree):
			edges.append((i, j))
		offset += degree
	
	# If this assertion fails, then the data provided in the degree stack is not a valid HCS tree
	assert(not degrees or len(degrees) == offset)
	return edges

def reconstruct_HCS_tree(file_base_name):
	"""Reconstruct the HCS tree by connecting each node to its children"""
	flatten = lambda x: [element for array in x for element in array]

	# Load degree information
	degree_file = open(file_base_name + '.degree', 'r')
	degree_by_level = [[int(degree_str) for degree_str in line.strip().split(',')] for line in degree_file.readlines()]
	degree_file.close()

	# Generate depth attribute information
	depths = flatten([[depth] * len(degrees) for depth, degrees in enumerate(degree_by_level)])

	# Flatten degree attribute information
	degrees = flatten(degree_by_level)

	# Generate tree
	g = igraph.Graph(directed = True)
	g.add_vertices(len(degrees))
	g.add_edges(reconstruct_community_edges(degrees))

	# Add attributes to nodes
	ids_by_depth = []
	for i, v in enumerate(g.vs()):
		if depths[i] >= len(ids_by_depth): ids_by_depth.append([])
		ids_by_depth[depths[i]].append(i)
		v['depth' ] = depths[i]
		v['degree'] = degrees[i]

	return g, ids_by_depth

def load_parameter(g, file_base_name, parameter):
	# Add attribute to nodes
	param_file = open(file_base_name + '.' + parameter, 'r')
	param_values = [float(param_str) for line in param_file.readlines() for param_str in line.strip().split(',')]
	param_file.close()
	for i, v in enumerate(g.vs()): v[parameter] = param_values[i]

def get_non_leaf_ids(g, ids):
	return filter(lambda id: g.outdegree(id), ids)

def get_leaf_ids(g, ids):
	return filter(lambda id: not g.outdegree(id), ids)

def get_param_average(g, param, ids):
	return float('nan') if len(ids) == 0 else sum([g.vs()[i][param] for i in ids]) / float(len(ids))

def get_param_average_by_level(g, param, ids_by_depth):
	return [get_param_average(g, param, ids) for ids in ids_by_depth]

def tree_query(g, all_ids_by_depth):
	# IDs for computing averages
	all_ids               = range(g.vcount())
	leaf_ids              = get_leaf_ids    (g, all_ids)
	non_leaf_ids          = get_non_leaf_ids(g, all_ids)
	leaf_ids_by_depth     = [get_leaf_ids    (g, ids    ) for ids in ids_by_depth]
	non_leaf_ids_by_depth = [get_non_leaf_ids(g, ids    ) for ids in ids_by_depth]

	# Compute derived parameters
	parameters.append('inter_edges/inter_vars')
	for v in g.vs():
		v['inter_edges/inter_vars'] = float('nan') if v['inter_vars'] == 0 else v['inter_edges'] / v['inter_vars']

	# Compute and output averages
	padding = max(len(param) for param in parameters)

	print("\nAverage parameter values:")
	for param in parameters: print("{}: {}".format(param.ljust(padding), get_param_average(g, param, all_ids)))

	print("\nAverage leaf parameter values:")
	for param in parameters: print("{}: {}".format(param.ljust(padding), get_param_average(g, param, leaf_ids)))

	print("\nAverage non-leaf parameter values:")
	for param in parameters: print("{}: {}".format(param.ljust(padding), get_param_average(g, param, non_leaf_ids)))

	print("\nAverage parameter values per level:")
	for param in parameters: print("{}: {}".format(param.ljust(padding), get_param_average_by_level(g, param, all_ids_by_depth)))

	print("\nAverage leaf parameter values per level:")
	for param in parameters: print("{}: {}".format(param.ljust(padding), get_param_average_by_level(g, param, leaf_ids_by_depth)))

	print("\nAverage non-leaf parameter values per level:")
	for param in parameters: print("{}: {}".format(param.ljust(padding), get_param_average_by_level(g, param, non_leaf_ids_by_depth)))

if __name__ == '__main__':
	# Input verification
	if len(sys.argv) != 2:
		print("Usage: python {} <CNF_PATH>".format(sys.argv[0]))
		exit()
	
	base_file_name = sys.argv[1]

	# Reconstruct HCS tree
	hcs_tree, ids_by_depth = reconstruct_HCS_tree(base_file_name)

	# Load parameters (skip depth and degree)
	for param in parameters[2:]: load_parameter(hcs_tree, base_file_name, param)

	# Query the tree
	tree_query(hcs_tree, ids_by_depth)
