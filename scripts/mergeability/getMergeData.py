import glob
import os
import sys

def getInstanceData(direc):
    ret = []
    for filename in os.listdir(direc):
        if filename.endswith('_merge.log'):
            f = open(os.path.join(direc, filename), "r").readlines()
            num_merges = int(f[6].split(',')[1])
            num_merge_pairs = int(f[7].split(',')[1])
            num_flips = int(filename.split('/')[-1].split('_')[0])
            ret.append((num_flips, num_merges, num_merge_pairs))

    ret = sorted(ret, key=lambda x: x[0])
    return ret


if len(sys.argv) != 2:
    print('USAGE: verifyMerge.py DIRECTORY')

f = open("mergeData.log", "w+")

maindir = sys.argv[1]
alldirs = [os.path.join(maindir, x) for x in os.listdir(maindir) if os.path.isdir(os.path.join(maindir, x))]
for col, dirname in enumerate(alldirs):
    data = getInstanceData(dirname)
    instance = dirname.split('/')[-1]
    
    ##f.write('instance: ' + instance + '\n')
    for row, d in enumerate(data):
        f.write(str(d[0]).strip() + " " + str(d[1]).strip() + " " + str(d[2]).strip() + "\n")

    f.write('\n\n')
f.close()
    
