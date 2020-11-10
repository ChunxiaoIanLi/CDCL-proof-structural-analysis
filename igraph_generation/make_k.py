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

new_lines = ''
for vertex in range(1, num_vars + 1):
    new_lines += str(vertex + 1) + ' '
    start = (k - 1) * vertex + num_vars
    end = (k - 1) * (vertex + 1) + num_vars
    for x in range(start, end):
        new_lines += str(x + 1) + ' '
    new_lines += '0 \n'

new_num_vars = k * num_vars
new_filename = filename.split('.')[0] + '_k.cnf'
new_file = open(new_filename, 'w+')
replaced = False
for index, line in enumerate(file):
    if not replaced and line.split(' ')[0] == 'p':
        new_file.write('p cnf ' + str(new_num_vars) + ' ' + line.split(' ')[3])
    else:
        replace = True
        new_file.write(line)

file.close()
new_file.close()
