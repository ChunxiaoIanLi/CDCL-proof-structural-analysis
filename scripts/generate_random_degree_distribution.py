import sys
import math
import os
import random

n=int(sys.argv[1])
m=int(sys.argv[2])
k=int(sys.argv[3])


def generateConstantPowerVec(n, m, k, beta):
    pd = []
    sum = 0
    for i in range(n):
        weight = (i+1)**(beta)
        pd.append(weight)
        sum += weight

    vec = []
    current_total = 0
    #generating vec from powerlaw
    for i in range(n):
        temp = int((pd[i]/float(sum))*m*k)
        vec.append(temp)
        current_total += temp

    #distribute remainders randomly
    for i in range(m*k - current_total):
        vec[random.randint(0, n-1)]+=1

    return vec


def generateBalancedVec(n, m, k):
    ave = int(m*k/n)
    remainder= int((m*k)%n)
    vec = [ave]*n
    while remainder > 0:
        vec[remainder-1]+=1
        remainder-=1
    return vec

def generateUnbalancedVec(n, m, k):
    vec=generateBalancedVec(int(n/2), m, k)
    
    for i in range(len(vec)):
        vec[i]-=1
        vec.append(1)

    if n%2 == 1:
        vec[(m*k)%(n/2)-1]-=1
        vec.append(1)
    return vec

def generateMediumVec(n, m, k):
    #somehow vec[0] is not modified after this call?
    vec=generateUnbalancedVec(n, m, k)
    max=vec[0]-2
    for i in range(n/2):
        diff=random.randint(0, max)
        vec[i]-=diff
        vec[-i]+=diff
    return vec

def generateCummulative(vec):
    cummulative_vec=[vec[0]]
    for i in vec[1:]:
        cummulative_vec.append(i + cummulative_vec[-1] + 1)
    return cummulative_vec

def vecsum(vec):
    sum = 0
    for i in vec:
        sum+=i
    return sum

def vecToString(vec):
    s = "c ["
    for i in vec:
        s+="{}, ".format(i)
    s = s[:-2]
    s += "]\n"
    return s

def generate_clause(m, k, cummulative_vec, variable_occur):
    clause = []
    for lit in range(k):
        found = False
        while not found:
            r = random.randint(0, m*k)
            for i in range(len(cummulative_vec)):
                if r <= cummulative_vec[i]:
                    if i+1 not in clause and (i+1)*-1 not in clause:
                        found = True
                        polarity=random.randint(0,1)
                        if polarity == 0:
                            clause.append((i+1)*-1)
                        else:
                            clause.append(i+1)
                        variable_occur[i]+=1
                        break;
                    break;
    return clause, variable_occur


def generateRandomFormula(n, m, k, cummulative_vec, outf):
    variable_occur = [0]*n
    cnf = []
    for clause in range(m):
        clause, variable_occur = generate_clause(m, k, cummulative_vec, variable_occur)
        cnf.append(clause)

    new_var_map=[-1]*n
    new_var=1
    for var in range(len(variable_occur)):
        if variable_occur[var] > 0:
            new_var_map[var] = new_var
            new_var+=1

    for clause in cnf:
        for variable in range(len(clause)):
            if clause[variable] > 0:
                clause[variable] = new_var_map[abs(clause[variable])-1]
            else:
                clause[variable] = new_var_map[abs(clause[variable])-1]*-1
        

    # compute actual number of variables
    actual_n = 0
    for i in variable_occur:
        if i > 0:
            actual_n += 1

    assert actual_n == new_var - 1

    header = "p cnf {0} {1}\n".format(actual_n, m)
    outstr = vecToString(variable_occur) + header
    outf.write(outstr)

    for clause in cnf:
        outstr = ""
        for variable in clause:
            outstr += str(variable) + " "
        outstr += "0\n"
        outf.write(outstr)
    return

balancedvec=generateBalancedVec(n, m, k)
unbalancedvec=generateUnbalancedVec(n, m, k)
constantpowerneg3vec=generateConstantPowerVec(n, m, k, -3)
constantpowerneg2point5vec=generateConstantPowerVec(n, m, k, -2.5)
constantpowerneg2vec=generateConstantPowerVec(n, m, k, -2)
constantpower2vec=generateConstantPowerVec(n, m, k, 2)
constantpower2point5vec=generateConstantPowerVec(n, m, k, 2.5)
constantpower3vec=generateConstantPowerVec(n, m, k, 3)

num_of_instanes = 200
if os.path.exists("balanced") and len(os.listdir('balanced') ) == 0:
    cummulative_vec=generateCummulative(balancedvec)
    for i in range(num_of_instanes):
        outf=open("balanced/{0}.cnf".format(i),"w")
        generateRandomFormula(n, m, k, cummulative_vec, outf)
        outf.close()
if os.path.exists("unbalanced") and len(os.listdir('unbalanced') ) == 0:
    cummulative_vec=generateCummulative(unbalancedvec)
    for i in range(num_of_instanes):
        outf=open("unbalanced/{0}.cnf".format(i),"w")
        generateRandomFormula(n, m, k, cummulative_vec, outf)
        outf.close()
if os.path.exists("medium") and len(os.listdir('medium') ) == 0:
    for i in range(num_of_instanes):
        mediumvec=generateMediumVec(n, m, k)
        cummulative_vec=generateCummulative(mediumvec)
        outf=open("medium/{0}.cnf".format(i),"w")
        generateRandomFormula(n, m, k, cummulative_vec, outf)
        outf.close()


