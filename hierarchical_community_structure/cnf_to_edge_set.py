def read_file(file):
	f=open("{0}".format(file),"r")
	#skip lines until header
	line = f.readline()
	line = line.split(" ")
	while line[0] != 'p' or line[1] != 'cnf':
		line = f.readline()
		line = line.split(" ")
	n = int(line[2])
	m = int(line[3])
	#store clauses in a list
	clauses=[]
	line = f.readline()
	while line:
		if line[0] != 'c':
			l = line.strip().split(" ")
			clauses.append(l[0:-1])
		line = f.readline()
	f.close()
	return clauses, m, n


def cnf_to_edge_set(clauses):
	edge_list = []
	for clause in clauses:
		for i in range(len(clause)-1):
			for j in range(i+1, len(clause)):
				edge_list.append([abs(int(clause[i]))-1, abs(int(clause[j]))-1])
	edge_set = set(map(frozenset, edge_list))
	return edge_set

# import itertools

def cnf_to_clauses_list(clauses):
	#[1, 2, 3, 0, 4, 2, 1, 0 ...]
	clauses_list = []
	for clause in clauses:
		for lit in clause:
			clauses_list.append(int(lit))
		clauses_list.append(0)
	return clauses_list










