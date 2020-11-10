import sys
from shutil import copyfile

filename = sys.argv[1]
k = int(sys.argv[2])
file = open(filename, 'r')

for line in file.readlines():
    if line[0] == 'c':
        continue
    if line[0] == 'p':
        num_vars = int(line.split(' ')[2])
        break

file.close()

new_lines = ''
for vertex in range(1, num_vars + 1):
    new_lines += str(vertex) + ' '
    start = (k - 1) * vertex + num_vars
    end = (k - 1) * (vertex + 1) + num_vars
    for x in range(start, end):
        new_lines += str(x) + ' '
    new_lines += '0 \n'

new_filename = filename.split('.')[0] + '_k.cnf'
copyfile(filename, new_filename)
file = open(new_filename, 'a')
file.write(new_lines)
file.close()
