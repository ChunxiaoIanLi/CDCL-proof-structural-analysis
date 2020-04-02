import sys
import math
import os
import random

n=int(sys.argv[1])
m=int(sys.argv[2])
k=int(sys.argv[3])


def generateUniformVec(n, m, k):
    ave = int(m*k/n)
    remainder= int((m*k)%n)
    vec = [ave]*n
    while remainder > 0:
        vec[remainder-1]+=1
        remainder-=1
    return vec

def generatePowerlawVec(n, m, k):
    vec=generateUniformVec(int(n/2), m, k)
    
    for i in range(len(vec)):
        vec[i]-=1
        vec.append(1)

    if n%2 == 1:
        vec[(m*k)%(n/2)-1]-=1
        vec.append(1)
    return vec

def generateMediumVec(n, m, k):
    #somehow vec[0] is not modified after this call?
    vec=generatePowerlawVec(n, m, k)
    max=vec[0]-2
    for i in range(n/2):
        diff=random.randint(0, max)
        vec[i]-=diff
        vec[-i]+=diff
    return vec

def generateCummulative(vec):
    cummulative_vec=[vec[0]]
    for i in vec[1:]:
        cummulative_vec.append(i + cummulative_vec[-1])
    return cummulative_vec

def vecsum(vec):
    sum = 0
    for i in vec:
        sum+=i
    return sum

def generateRandomFormula(n, m, k, cummulative_vec, outf):
    outstr=""
    for clause in range(m):
        temp_clause = []
        for lit in range(k):
            found = False
            while not found:
                r = random.randint(0, m*k)
                for i in range(len(cummulative_vec)):
                    if r <= cummulative_vec[i]:
                        if i+1 not in temp_clause:
                            temp_clause.append(i+1)
                            found = True
                            polarity=random.randint(0,1)
                            if polarity == 0:
                                outstr+="-"
                            outstr+=str(i+1)
                            outstr+=" "
                            break;
                        break;
        outstr+="0\n"
        outf.write(outstr)
        outstr=""
    return

if not os.path.exists("instances"):
    os.makedirs("instances")
    if not os.path.exists("instances/uniform"):
        os.makedirs("instances/uniform")
    if not os.path.exists("instances/powerlaw"):
        os.makedirs("instances/powerlaw")
    if not os.path.exists("instances/medium"):
        os.makedirs("instances/medium")   


#print(uniformvec, vecsum(uniformvec))
#print(powerlawvec, vecsum(powerlawvec))
#print(randomvec, vecsum(randomvec))

#generating uniform
uniformvec=generateUniformVec(n, m, k)
cummulative_vec=generateCummulative(uniformvec)
for i in range(200):
    outf=open("instances/uniform/{0}.cnf".format(i),"w")
    outf.write("p cnf {0} {1}\n".format(n, m))
    generateRandomFormula(n, m, k, cummulative_vec, outf)
    outf.close()

# #generating powerlaw
powerlawvec=generatePowerlawVec(n, m, k)
cummulative_vec=generateCummulative(powerlawvec)
for i in range(200):
    outf=open("instances/powerlaw/{0}.cnf".format(i),"w")
    outf.write("p cnf {0} {1}\n".format(n, m))
    generateRandomFormula(n, m, k, cummulative_vec, outf)
    outf.close()

# #generating medium
for i in range(200):
    mediumvec=generateMediumVec(n, m, k)
    cummulative_vec=generateCummulative(mediumvec)
    outf=open("instances/medium/{0}.cnf".format(i),"w")
    outf.write("p cnf {0} {1}\n".format(n, m))
    generateRandomFormula(n, m, k, cummulative_vec, outf)
    outf.close()



