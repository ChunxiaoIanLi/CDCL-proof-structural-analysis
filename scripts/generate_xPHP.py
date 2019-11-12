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

def generateExtended(n, currentn, outf):
    #new extended variable are assgined an integer starting from Qstarting
    #variables starting from previous level starts from Pstarting 
    Pstarting=0
    Qstarting=n*(n-1)
    for i in range(n, currentn, -1):
        Pstarting+=i*(i-1)
        Qstarting+=(i-1)*(i-2)

    outstr=""
    #for each extended variables
    for i in range(1, currentn):
        for j in range(1, currentn-1):
            Qij=str(Qstarting+(i-1)*(currentn-2)+j)
            Pij=str(Pstarting+(i-1)*(currentn-1)+j)
            Pin1=str(Pstarting+(i-1)*(currentn-1)+currentn-1)
            Pnj=str(Pstarting+(currentn-1)*(currentn-1)+j)
            outstr+=Qij+" -"+Pij+" 0\n"
            outstr+=Qij+" -"+Pin1+" -"+Pnj+" 0\n"
            outstr+="-"+Qij+" "+Pij+" "+Pin1+" 0\n"
            outstr+="-"+Qij+" "+Pij+" "+Pnj+" 0\n"
            outf.write(outstr)
            outstr=""
    if currentn!=3:
        generateExtended(n, currentn-1, outf)
    return

if not os.path.exists("extended_instances"):
    os.makedirs("extended_instances")
outf=open("extended_instances/x{0}.cnf".format(n),"w")

nVar=0
for i in range(n, 1, -1):
    nVar+=i*(i-1)
nClause=n+(n-1)*(n-1+1)*(n-1)/2
for i in range(n-1, 1, -1):
    nClause+=4*i*(i-1)

outf.write("p cnf {0} {1}\n".format(nVar, nClause))

generatePHP(n, outf)
generateExtended(n, n, outf)

outf.close()

