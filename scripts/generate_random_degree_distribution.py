import sys
import math
import os
import random

n=int(sys.argv[1])
m=int(sys.argv[2])
k=int(sys.argv[3])


def generateLowVec(n, m, k):
    ave = int(m*k/n)
    remainder= int((m*k)%n)
    vec = [ave]*n
    while remainder > 0:
        vec[remainder-1]+=1
        remainder-=1
    return vec

def generateHighVec(n, m, k):
    vec=generateLowVec(int(n/2), m, k)
    
    for i in range(len(vec)):
        vec[i]-=1
        vec.append(1)

    if n%2 == 1:
        vec[(m*k)%(n/2)-1]-=1
        vec.append(1)
    return vec

def generateMediumVec(n, m, k):
    #somehow vec[0] is not modified after this call?
    vec=generateHighVec(n, m, k)
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
        for lit in range(k):
            r = random.randint(0, m*k)
            for i in range(len(cummulative_vec)):
                if r <= cummulative_vec[i]:
                    polarity=random.randint(0,1)
                    if polarity == 0:
                        outstr+="-"
                    outstr+=str(i+1)
                    outstr+=" "
                    break;
        outstr+="0\n"
        outf.write(outstr)
        outstr=""
    return

if not os.path.exists("instances"):
    if not os.path.exists("instances/low"):
        os.makedirs("instances/low")
    if not os.path.exists("instances/high"):
        os.makedirs("instances/high")
    if not os.path.exists("instances/medium"):
        os.makedirs("instances/medium")   

lowvec=generateLowVec(n, m, k)
highvec=generateHighVec(n, m, k)
mediumvec=generateMediumVec(n, m, k)

#print(lowvec, vecsum(lowvec))
#print(highvec, vecsum(highvec))
#print(mediumvec, vecsum(mediumvec))

#generating low
cummulative_vec=generateCummulative(lowvec)
for i in range(1):
    outf=open("instances/low/{0}.cnf".format(i),"w")
    outf.write("p cnf {0} {1}\n".format(n, m))
    generateRandomFormula(n, m, k, cummulative_vec, outf)
    outf.close()

# #generating high
cummulative_vec=generateCummulative(lowvec)
for i in range(1):
    outf=open("instances/high/{0}.cnf".format(i),"w")
    outf.write("p cnf {0} {1}\n".format(n, m))
    generateRandomFormula(n, m, k, cummulative_vec, outf)
    outf.close()

# #generating medium
cummulative_vec=generateCummulative(lowvec)
for i in range(1):
    outf=open("instances/medium/{0}.cnf".format(i),"w")
    outf.write("p cnf {0} {1}\n".format(n, m))
    generateRandomFormula(n, m, k, cummulative_vec, outf)
    outf.close()



