import matplotlib.pyplot as plt
import sys
import numpy as np


filename = sys.argv[1]
f = open(filename, "r")

running_times = []
for line in f.readlines():
    running_times.append(float(line[line.strip().find(":")+1:line.find("s")]))

plt.hist(running_times, density=True, bins=30)
plt.title(filename)
plt.locator_params(axis='x', nbins=10)
plt.ylabel('Occurrences')
plt.xlabel('Running Time')

plt.savefig(filename[:filename.find(".")] + '.svg')
