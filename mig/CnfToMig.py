def resolvable(c1, c2):
    for lit1 in c1:
        if -lit1 in c2:
            return True
    return False

def share_literal(c1, c2):
    for lit1 in c1:
        if lit1 in c2:
            return True
    return False

in_file = './test.cnf'
cnf_clauses = []
for id, line in enumerate(open(in_file, 'r').readlines()[1:]):
    cnf_clauses.append([list(map(int, line.split(' ')[:-1])), id])

mig_clauses = []
index = 0
for clause1, id1 in cnf_clauses:
    for clause2, id2 in cnf_clauses[index + 1:]:
        if resolvable(clause1, clause2):
            if share_literal(clause1, clause2):
                mig_clauses.append([id1, id2])
    index += 1

vertices_set = []
for clause in mig_clauses:
    vertices_set = vertices_set + clause
vertices_count = len(set(vertices_set))
out_file = './out.gr'
with open(out_file, 'w+') as f:
    f.write('p tw '+ str(vertices_count) + ' ' + str(len(mig_clauses)) + '\n')
    for clause in mig_clauses:
        str_clause = list(map(str, clause))
        f.write(' '.join(str_clause) + '\n')
    
print('conversion finished!')
