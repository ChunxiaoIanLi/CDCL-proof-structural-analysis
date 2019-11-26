import os
import sys


inpath=sys.argv[1]
infile=sys.argv[2]
outfull=inpath+"/"+infile+".gr"

infp=open(inpath+infile, "r")
outfp=open(outfull, "w")

vertices=0
edges=0
outstring=""

while True:
    l = infp.readline().strip()
    if not l:
        break
    line = l.split(' ')
    learntID=int(line[0])
    if learntID > vertices:
        vertices = learntID
    for antecedentID in reversed(line[:-1]):
        if int(antecedentID) == 0:
            break
        outstring+=str(int(antecedentID))+" "+str(int(learntID))+"\n"
        edges+=1

header="p tw "+str(vertices)+" "+str(edges)+"\n"
outfp.write(header)
outfp.write(outstring)

infp.close()
outfp.close()
