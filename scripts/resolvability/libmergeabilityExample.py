# Use ctypes to call our C/C++ code
import ctypes
lib = ctypes.CDLL('./libmergeability.so')

# An object for working with the C/C++ library
class PMI(object):
	def __init__(self):
		self.obj = lib.PMI_init()

	def setClauses(self, clauses):
		arr = (ctypes.c_longlong * len(clauses))(*clauses)
		lib.PMI_setClauses.argtypes = [ ctypes.c_void_p, ctypes.c_longlong * len(clauses), ctypes.c_longlong ]
		lib.PMI_setClauses(self.obj, arr, len(clauses))

	def calculateMergeability(self, varSet):
		arr = (ctypes.c_longlong * len(varSet))(*varSet)
		lib.PMI_calculateMergeability.argtypes = [ ctypes.c_void_p, ctypes.c_longlong * len(varSet) ]
		lib.PMI_calculateMergeability(self.obj, arr)

	# Normalize mergeability score by total number of resolvable pairs
	def getMergeabilityScoreNorm1(self):
		lib.PMI_getMergeabilityScoreNorm1.argtypes = [ ctypes.c_void_p ]
		return lib.PMI_getMergeabilityScoreNorm1(self.obj)

	# Normalize mergeability score by m^2
	def getMergeabilityScoreNorm2(self):
		lib.PMI_getMergeabilityScoreNorm2.argtypes = [ ctypes.c_void_p ]
		return lib.PMI_getMergeabilityScoreNorm2(self.obj)

# Configure ctypes to work with library functions
lib.PMI_setClauses.restype = None
lib.PMI_calculateMergeability.restype = None
lib.PMI_getMergeabilityScoreNorm1.restype = ctypes.c_double
lib.PMI_getMergeabilityScoreNorm2.restype = ctypes.c_double

# Create object
pmi = PMI()

# Put the clauses in dimacs format
clauses = [1,2,3,4,5,0,-1,5,7,8,0,-2,3,5,6,7,0]
numVars = 8

# Load the clauses
pmi.setClauses(clauses)

# Put the variable set in a zero-terminated array
varSet = [1,2,3,4,5,6,7,8,0]

# Calculate mergeability
pmi.calculateMergeability(varSet)
print pmi.getMergeabilityScoreNorm1()
print pmi.getMergeabilityScoreNorm2()
print "------"
pmi.calculateMergeability([1,2,3,4,5,6,7,0])
print pmi.getMergeabilityScoreNorm1()
print pmi.getMergeabilityScoreNorm2()
print "------"
pmi.calculateMergeability([1,3,5,6,7,0])
print pmi.getMergeabilityScoreNorm1()
print pmi.getMergeabilityScoreNorm2()
