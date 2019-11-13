import sys
import math
import os

n=int(sys.argv[1])

def generatePHP(n, outf):
    outstr=""
    #for each pigeon clause                                                           
    for i in range(1, n+1):
        for j in range(1, n):
            Pij=str((i-1)*(n-1)+j)
            outstr+=Pij
            outstr+=" "
        outstr+="0\n"
        outf.write(outstr)
        outstr=""

    #for each hole clause                                                             
    for k in range(1, n):
        for j in range(1, n+1):
            for i in range(1,j):
                Pik=str((i-1)*(n-1)+k)
                Pjk=str((j-1)*(n-1)+k)
                outstr+="-"+Pik+" -"+Pjk+" 0\n"
                outf.write(outstr)
                outstr=""
    return

if not os.path.exists("instances"):
    os.makedirs("instances")
outf=open("instances/{0}.cnf".format(n),"w")

nVar=n*(n-1)
nClause=n+(n-1)*(n-1+1)*(n-1)/2
outf.write("p cnf {0} {1}\n".format(nVar, nClause))
generatePHP(n, outf)

outf.close()

