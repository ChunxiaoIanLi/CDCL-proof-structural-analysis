import os
import sys
import re


def main(argv):
    path = argv[1]

    file = open(path + '/all_fitted_data.log', 'w+')

    for filename in os.listdir(path):
        if filename.endswith('_fitted.log'):
            fitted_file = open(os.path.join(path, filename))
            fitted_lines = fitted_file.readlines()
            equation = fitted_lines[0].split(' ')[0] + '*(x^-' + fitted_lines[0].split()[1] + ')'
            file.write(re.sub('_fitted.log', '', filename) + ', ' + equation + '\n')


if __name__ == "__main__":
    main(sys.argv)
