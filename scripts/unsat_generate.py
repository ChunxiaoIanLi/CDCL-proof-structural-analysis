import os
import sys
import math
import random

def generateClause(vars):
    clause = []
    for i in range(3):
        randvar = random.randrange(1, vars+1)
        while randvar in clause:
            randvar = random.randrange(1, vars+1)
        if random.random() < 0.5:
            clause.append(randvar)
        else:
            clause.append(randvar*-1)
    clause.sort()
    return clause
    

vars=int(sys.argv[1])
cvr=int(sys.argv[2])
c=cvr * vars

print("p cnf {} {}".format(vars, c))

clauses = []

for i in range(c):
    clause = generateClause(vars)
    while clause in clauses:
        clause = generateClause(vars)

    clauses.append(clause)
        
    outstr = ""
    for var in clause:
        outstr += str(var) + " "
    outstr += "0"
    print(outstr)
    out = []
        
