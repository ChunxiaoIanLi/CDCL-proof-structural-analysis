from PMILib import PMI
from cnf_to_edge_set import read_file, cnf_to_clauses_list

def param_expect(index, expectedMergeability, expectedResolvability):
	# Create object
	pmi = PMI()

	# Load clauses from file
	clauses, m, n = read_file("mergeability_test_suite/{}.cnf".format(index))
	clause_list = cnf_to_clauses_list(clauses)
	pmi.setClauses(clause_list)

	# Get variable set
	varset = range(1, n + 1)
	varset.append(0)

	# Calculate stats
	pmi.calculate(varset, 0)
	resolvability = pmi.getResolvability()
	mergeability = pmi.getMergeability()
	if (expectedMergeability != mergeability) or (expectedResolvability != resolvability):
		print("Test {} failed: actual <m,r> = <{},{}>; expected <m,r> = <{},{}>".format(index, mergeability, resolvability, expectedMergeability, expectedResolvability))
		return 1
	return 0

if __name__ == "__main__":
	testResults = 0

	testResults += param_expect( 1,  0,  0)
	testResults += param_expect( 2,  0,  3)
	testResults += param_expect( 3,  0,  2)
	testResults += param_expect( 4,  0, 10)
	testResults += param_expect( 5,  0, 10)
	testResults += param_expect( 6,  0, 19)
	testResults += param_expect( 7,  5,  5)
	testResults += param_expect( 8,  5,  5)
	testResults += param_expect( 9, 10, 10)
	testResults += param_expect(10, 10, 10)
	testResults += param_expect(11,  5, 10)
	testResults += param_expect(12,  5, 10)
	testResults += param_expect(13,  5, 19)
	testResults += param_expect(14, 19, 19)
	testResults += param_expect(15,  0,  9)
	testResults += param_expect(16,  4,  9)
	testResults += param_expect(17,  2,  9)
	testResults += param_expect(18,  5, 10)
	testResults += param_expect(19,  0, 10)
	testResults += param_expect(20,  5,  5)
	testResults += param_expect(21,  4, 11)
	testResults += param_expect(22,  5, 10)
	testResults += param_expect(23, 19, 19)

	totalNumTests = 23
	print("{}/{} tests passed".format(totalNumTests - testResults, totalNumTests))