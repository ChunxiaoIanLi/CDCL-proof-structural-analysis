# Use ctypes to call our C/C++ code
import ctypes
lib = ctypes.CDLL('./libmergeability.so');

# Put the clauses in dimacs format
clauses = [1,2,3,4,0,-1,5,7,8,0,-2,3,5,6,7,0]
numVars = 9

# This part handles formatting the data in a way it can be passed to the C/C++ function
lib.calculateMergeability.restype = ctypes.c_longlong
lib.calculateMergeability.argtypes = [ ctypes.c_longlong * len(clauses), ctypes.c_longlong ]
arr = (ctypes.c_longlong * len(clauses))(*clauses)
mrg = lib.calculateMergeability(arr, numVars, len(clauses))

print mrg
