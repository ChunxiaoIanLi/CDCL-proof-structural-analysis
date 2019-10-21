from __future__ import division
import os
import sys
import math
import random

levels=int(sys.argv[1])
degree=int(sys.argv[2])

nofInternalnodes = 0
for h in range(levels-1):
	nofInternalnodes+=degree**h
nofEdge = 0

final = ""

for v in range(1, nofInternalnodes+1):
	for i in range(degree-1, -1, -1):
		final+="{} {}\n".format(v*degree + 1 - i, v)
		nofEdge+=1
		
print("p tw {} {}".format(int((levels+1)*levels/2), nofEdge))
print(final)
