import sys

in_file = sys.argv[1]
out_file = sys.argv[2]
cnf_clauses = [None]
for id, line in enumerate(open(in_file, 'r').readlines()[1:]):
    if line[0] != 'c':
        cnf_clauses.append(list(map(int, line.split(' ')[:-1])))

clause_list = {}
for id, clause in enumerate(cnf_clauses):
    if id == 0:
        continue
    for lit in clause:
        if lit in clause_list:
            clause_list[lit].append(id)
        else:
            clause_list[lit] = [id]


mig_clauses = []
for var in clause_list.keys():
    clauses = clause_list[var]

    for idx1, clause_idx1 in enumerate(clauses):
        clause1 = cnf_clauses[clause_idx1]

        for clause_idx2 in clauses[idx1 + 1:]:
            for lit in clause1:
                if lit*-1 in clause_list and clause_idx2 in clause_list[lit*-1]:
                    mig_clauses.append([clause_idx1, clause_idx2])
        
vertices_set = []
for clause in mig_clauses:
    vertices_set = vertices_set + clause
vertices_count = len(set(vertices_set))

with open(out_file, 'w+') as f:
    f.write('p tw '+ str(vertices_count) + ' ' + str(len(mig_clauses)) + '\n')
    for clause in mig_clauses:
        str_clause = list(map(str, clause))
        f.write(' '.join(str_clause) + '\n')
    
print('conversion finished!')
