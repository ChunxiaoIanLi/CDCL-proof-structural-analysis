from __future__ import division
import os
import sys
import math
import random


levels=int(sys.argv[1])

nofEdge = 0

final = ""
for i in range(levels):
	for j in range(levels-i-1):
		v1 = int(i*(levels+levels-i+1)/2+j+1)
		if i < levels - 3:
			visited = []
			while random.random() < (levels - i)/(2*levels):
				v2 = int(random.random()*(levels-i)*(levels-i-1)/2 + (i+1)*(levels+levels-i)/2 + 1)
				while v2 in visited:
					v2 = int(random.random()*(levels-i)*(levels-i-1)/2 + (i+1)*(levels+levels-i)/2 + 1)
				visited.append(v2)
				#final+="{} {} 0\n".format(v1, v2)
				final+="{} {}\n".format(v1, v2) 
				nofEdge+=1

		v2 = int((i+1)*(levels+levels-i)/2+j+1)
		if random.random() > 0.05:
	 		#final+="{} {} 0\n".format(v1, v2)
			final+="{} {}\n".format(v1, v2)
	 		nofEdge+=1
	 	elif i > levels-3:
	 		#final+="{} {} 0\n".format(v1, v2)
	 		final+="{} {}\n".format(v1, v2)
			nofEdge+=1
	 	if random.random() > 0.05:	
	 		#final+="{} {} 0\n".format(v1+1, v2)
	 		final+="{} {}\n".format(v1, v2)
			nofEdge+=1
	 	elif i > levels-3:
	 		#final+="{} {} 0\n".format(v1, v2)
	 		final+="{} {}\n".format(v1, v2)
			nofEdge+=1

#print("p cnf {} {}".format(int((levels+1)*levels/2), nofEdge))
print("p tw {} {}".format(int((levels+1)*levels/2), nofEdge))
print(final)
