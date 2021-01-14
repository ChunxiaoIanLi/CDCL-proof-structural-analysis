import sys
import igraph
from VIG_to_CNF import VIG_to_CNF
from HCS_to_CNF import g_to_svg
from cnf_to_edge_set import cnf_to_edge_set, read_file
from os import walk, path


def isomorphic(dir_name, file, m, k):
    # convert original cnf to vig
    clauses_orig, temp_orig, n = read_file(path.join(dir_name, file))
    edge_set_orig = cnf_to_edge_set(clauses_orig)
    edge_list_orig = [list(e) for e in edge_set_orig]
    g_orig = igraph.Graph()
    g_orig.add_vertices(n)
    g_orig.add_edges(edge_list_orig)

    # call VIG_to_CNF code on original cnf
    g_temp = g_orig.copy()
    g_to_svg(g_temp)
    cnf_out = VIG_to_CNF(g_temp, m, k)

    # convert the new cnf to vig
    edge_set_out = cnf_to_edge_set(cnf_out)
    edge_list_out = [list(e) for e in edge_set_out]
    g_out = igraph.Graph()
    g_out.add_vertices(n)
    g_out.add_edges(edge_list_out)

    # check if original cnf and output cnf's graphs are isomorphic
    iso = g_orig.isomorphic(g_out)
    return iso

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('ERROR: call with arguments: file/dir name, m, k')

    file_or_dir = str(sys.argv[1])
    if not path.isfile(file_or_dir) and not path.isdir(file_or_dir):
        print('ERROR: arg 1 is not a file or directory')

    # m is the number of clauses in the CNF
    m = int(sys.argv[2])
    # k is the width of clauses
    k = int(sys.argv[3])


    files = []
    dir_name = ''
    if path.isdir(file_or_dir):
        dir_name = file_or_dir
        for (dirpath, dirnames, filenames) in walk(file_or_dir):
            for filename in filenames:
                if filename.endswith('.cnf'):
                    files.append(filename)
    else:
        files.append(file_or_dir)


    # run test for each file in list
    for file in files:
        iso = isomorphic(dir_name, file, m, k)

        if iso:
            print('Instance ' + file + ' is isomorphic')
        else:
            print('INSTANCE ' + file + ' IS NOT ISOMORPHIC')
