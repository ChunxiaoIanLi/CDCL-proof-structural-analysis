import HCS_to_CNF_direct
import generate_random_degree_distribution

class TestResult:
	def __init__(self, testResults = 0, totalNumTests = 0):
		self.testResults   = testResults
		self.totalNumTests = totalNumTests
	
	def __iadd__(self, other):
		self.testResults   += other.testResults
		self.totalNumTests += other.totalNumTests
		return self
	
	def result_str(self):
		return "{}/{} tests passed".format(self.totalNumTests - self.testResults, self.totalNumTests)

TEST_OKAY = TestResult(0, 1)
TEST_FAIL = TestResult(1, 1)

def expect(testResult, actual, expected):
	if actual == expected: return TEST_OKAY
	print("Test {} failed: <actual> = <{}>; <expected> = <{}>".format(testResult.totalNumTests, actual, expected))
	return TEST_FAIL

def test_get_n():
	def expect_get_n(testResult, subcnfs, expected_n):
		testResult += expect(testResult, HCS_to_CNF_direct.get_n(subcnfs), expected_n)

	testResult = TestResult()
	
	expect_get_n(testResult, [          ], 0)
	expect_get_n(testResult, [[1       ]], 1)
	expect_get_n(testResult, [[-1      ]], 1)
	expect_get_n(testResult, [[ 1,  2,  3]], 3)
	expect_get_n(testResult, [[-1, -2, -3]], 3)
	expect_get_n(testResult, [[ 3,  2,  1]], 3)
	expect_get_n(testResult, [[-3, -2, -1]], 3)
	expect_get_n(testResult, [[ 1, -3,  2]], 3)
	expect_get_n(testResult, [[1], [ 2], [3]], 3)
	expect_get_n(testResult, [[1], [-3], [2]], 3)
	expect_get_n(testResult, [[1, 3, 5], [2, 6, -3], [7, 4, 2]], 7)

	return testResult.result_str()

def test_combine_subcnfs():
	def expect_combine_subcnfs(testResult, subcnfs, expected_cnf, expected_upper_bounds):
		actual_cnf, actual_upper_bounds = HCS_to_CNF_direct.combine_subcnfs(subcnfs)
		testResult += expect(testResult, actual_cnf         , expected_cnf         )
		testResult += expect(testResult, actual_upper_bounds, expected_upper_bounds)

	testResult = TestResult()
	
	expect_combine_subcnfs(testResult, [                        ], [                    ], [0      ])
	expect_combine_subcnfs(testResult, [[[1]                   ]], [[1     ]            ], [0, 1   ])
	expect_combine_subcnfs(testResult, [[[1], [2]              ]], [[1], [2]            ], [0, 2   ])
	expect_combine_subcnfs(testResult, [[[1], [2]], [[ 1], [ 2]]], [[1], [2], [ 3], [ 4]], [0, 2, 4])
	expect_combine_subcnfs(testResult, [[[1], [2]], [[-1], [-2]]], [[1], [2], [-3], [-4]], [0, 2, 4])
	expect_combine_subcnfs(testResult, [[[1], [2], [3]],  [[-1]]], [[1], [2], [ 3], [-4]], [0, 3, 4])

	expect_combine_subcnfs(testResult,
		[[[1, 2, 3], [-1, 4, 2], [-2, 3, -4]], [[-3, -2], [1]], [[-1]]],
		[ [1, 2, 3], [-1, 4, 2], [-2, 3, -4],   [-7, -6], [5],   [-8] ],
		[0, 4, 7, 8]
	)

	return testResult.result_str()

def test_add_edges_to_combined_disconnected_cnfs():
	def expect_add_edges_to_combined_disconnected_cnfs(testResult,
		level, depth, inter_vars_fraction, community_id_upper_bounds, k, cnf,
		expected_num_inter_vars
	):
		# Since this function makes use of randomness, we just check graph invariants
		num_original_clauses = len(cnf)
		cnf = HCS_to_CNF_direct.add_edges_to_combined_disconnected_cnfs(level, depth, inter_vars_fraction, community_id_upper_bounds, k, cnf)
		
		# Remove original edges so that we are only left with the new edges
		new_clauses = cnf[num_original_clauses:]

		# All variables in new edges should be inter-community variables
		# Identify inter_vars
		inter_vars = set([abs(l) for c in new_clauses for l in c])

		# Check number of inter_vars
		testResult += expect(testResult, len(inter_vars), expected_num_inter_vars)

		# Check width of clauses
		success = True
		for clause in new_clauses:
			if len(clause) != k:
				print("Test {} failed: <actual width> = <{}>; <expected width> = <{}>".format(testResult.totalNumTests, len(clause), k))
				success = False
				break
		testResult += TEST_OKAY if success else TEST_FAIL

	testResult = TestResult()
	global cvr
	cvr = [1.]
	cnf = [[1, 2, 3], [-1, -2, 3], [2, 3], [4, 5, 6], [-4, 5, -6], [7, 8, 9], [10, -11, -12], [-8, 9, 11]]

	expect_add_edges_to_combined_disconnected_cnfs(testResult, 1, 1, 1/3., [0, 6, 12], 3, cnf[:], 4)
	expect_add_edges_to_combined_disconnected_cnfs(testResult, 1, 1, 1/2., [0, 6, 12], 3, cnf[:], 6)
	expect_add_edges_to_combined_disconnected_cnfs(testResult, 1, 1, 1/3., [0, 6, 12], 4, cnf[:], 4)
	expect_add_edges_to_combined_disconnected_cnfs(testResult, 1, 1, 1/2., [0, 6, 12], 4, cnf[:], 6)

	return testResult.result_str()

def test_generateUniformVec():
	def expect_generateUniformVec(testResult, n, m, k, expected_degree_vector):
		testResult += expect(testResult, generate_random_degree_distribution.generateUniformVec(n, m, k), expected_degree_vector)

	testResult = TestResult()

	expect_generateUniformVec(testResult, 5, 0, 3, [1] *  0 + [0] * 5)
	expect_generateUniformVec(testResult, 5, 1, 3, [1] *  3 + [0] * 2)
	expect_generateUniformVec(testResult, 5, 2, 3, [2] *  1 + [1] * 4)
	expect_generateUniformVec(testResult, 5, 3, 3, [2] *  4 + [1] * 1)
	expect_generateUniformVec(testResult, 5, 4, 3, [3] *  2 + [2] * 3)
	expect_generateUniformVec(testResult, 5, 5, 3, [3] *  5 + [2] * 0)

	expect_generateUniformVec(testResult, 10, 0, 3, [1] *  0 + [0] * 10)
	expect_generateUniformVec(testResult, 10, 1, 3, [1] *  3 + [0] *  7)
	expect_generateUniformVec(testResult, 10, 3, 3, [1] *  9 + [0] *  1)
	expect_generateUniformVec(testResult, 10, 4, 3, [2] *  2 + [1] *  8)
	expect_generateUniformVec(testResult, 10, 8, 3, [3] *  4 + [2] *  6)
	expect_generateUniformVec(testResult, 10, 4, 6, [3] *  4 + [2] *  6)
	expect_generateUniformVec(testResult, 10, 5, 2, [1] * 10 + [0] *  0)
	expect_generateUniformVec(testResult, 10, 5, 4, [2] * 10 + [1] *  0)
	expect_generateUniformVec(testResult, 10, 3, 3, [1] *  9 + [0] *  1)
	expect_generateUniformVec(testResult, 10, 7, 3, [3] *  1 + [2] *  9)

	return testResult.result_str()

def test_generatePowerlawVec():
	def expect_generatePowerlawVec(testResult, n, m, k, expected_degree_vector):
		testResult += expect(testResult, generate_random_degree_distribution.generatePowerlawVec(n, m, k), expected_degree_vector)

	testResult = TestResult()

	expect_generatePowerlawVec(testResult, 5, 0, 3, [1] * 0 + [0] * 5)
	expect_generatePowerlawVec(testResult, 5, 1, 3, [1] * 3 + [0] * 2)
	expect_generatePowerlawVec(testResult, 5, 2, 3, [2] * 1 + [1] * 4)
	expect_generatePowerlawVec(testResult, 5, 2, 4, [3] * 1 + [2] * 1 + [1] * 3)
	expect_generatePowerlawVec(testResult, 5, 7, 1, [2] * 2 + [1] * 3)
	expect_generatePowerlawVec(testResult, 5, 3, 3, [3] * 2 + [1] * 3)
	expect_generatePowerlawVec(testResult, 5, 4, 3, [5] * 1 + [4] * 1 + [1] * 3)
	expect_generatePowerlawVec(testResult, 5, 5, 3, [6] * 2 + [1] * 3)

	expect_generatePowerlawVec(testResult, 10,  0, 3, [1] *  0 + [0] * 10)
	expect_generatePowerlawVec(testResult, 10,  1, 3, [1] *  3 + [0] *  7)
	expect_generatePowerlawVec(testResult, 10,  3, 3, [1] *  9 + [0] *  1)
	expect_generatePowerlawVec(testResult, 10,  4, 3, [2] *  2 + [1] *  8)
	expect_generatePowerlawVec(testResult, 10,  5, 3, [2] *  5 + [1] *  5)
	expect_generatePowerlawVec(testResult, 10,  5, 2, [1] * 10 + [2] *  0)
	expect_generatePowerlawVec(testResult, 10,  5, 4, [3] *  5 + [1] *  5)
	expect_generatePowerlawVec(testResult, 10,  3, 6, [3] *  3 + [2] *  2 + [1] * 5)
	expect_generatePowerlawVec(testResult, 10,  7, 3, [4] *  1 + [3] *  4 + [1] * 5)
	expect_generatePowerlawVec(testResult, 10,  6, 3, [3] *  3 + [2] *  2 + [1] * 5)
	expect_generatePowerlawVec(testResult, 10,  6, 3, [3] *  3 + [2] *  2 + [1] * 5)

	return testResult.result_str()

def test_generateCumulative():
	def expect_generateCumulative(testResult, degree_vector, expected_cumulative_vector):
		testResult += expect(testResult, generate_random_degree_distribution.generateCummulative(degree_vector), expected_cumulative_vector)
	
	testResult = TestResult()

	expect_generateCumulative(testResult, [], [])
	expect_generateCumulative(testResult, [1], [1])
	expect_generateCumulative(testResult, [3, 2, 1], [3, 5, 6])
	expect_generateCumulative(testResult, [1, 2, 3], [1, 3, 6])
	expect_generateCumulative(testResult, [10, 5, 1], [10, 15, 16])
	expect_generateCumulative(testResult, [10, 15, 12], [10, 25, 37])

	return testResult.result_str()

def test_same_community():
	def expect_same_community(testResult, u, v, community_id_upper_bounds, expectation):
		testResult += expect(testResult, generate_random_degree_distribution.same_community(u, v, community_id_upper_bounds), expectation)
	
	testResult = TestResult()

	expect_same_community(testResult,  1,  1, [0, 1], True)
	expect_same_community(testResult,  1,  1, [0, 2], True)
	expect_same_community(testResult,  1,  2, [0, 2], True)
	expect_same_community(testResult,  1,  2, [0, 1, 2], False)
	expect_same_community(testResult,  2,  2, [0, 1, 2], True)
	expect_same_community(testResult, 10, 20, [0, 10, 20, 30, 40], False)
	expect_same_community(testResult, 10, 15, [0, 10, 20, 30, 40], True)
	expect_same_community(testResult, 15, 25, [0, 10, 20, 30, 40], False)
	expect_same_community(testResult, 24, 25, [0, 10, 20, 30, 40], True)
	expect_same_community(testResult, 25, 25, [0, 10, 20, 30, 40], True)
	expect_same_community(testResult,  9, 10, [0, 10, 20, 30, 40], True)
	expect_same_community(testResult, 10, 11, [0, 10, 20, 30, 40], False)
	expect_same_community(testResult,  9, 11, [0, 10, 20, 30, 40], False)
	expect_same_community(testResult, 19, 20, [0, 10, 20, 30, 40], True)
	expect_same_community(testResult, 20, 21, [0, 10, 20, 30, 40], False)
	expect_same_community(testResult, 19, 21, [0, 10, 20, 30, 40], False)

	return testResult.result_str()

def test_all_same_community():
	def expect_all_same_community(testResult, literals, community_id_upper_bounds, expectation):
		testResult += expect(testResult, generate_random_degree_distribution.all_same_community(literals, community_id_upper_bounds), expectation)

	testResult = TestResult()

	expect_all_same_community(testResult, [ 1,  1], [0, 1], True)
	expect_all_same_community(testResult, [-1,  1], [0, 1], True)
	expect_all_same_community(testResult, [ 1,  1], [0, 2], True)
	expect_all_same_community(testResult, [-1,  1], [0, 2], True)
	expect_all_same_community(testResult, [ 1,  2], [0, 1, 2], True)
	expect_all_same_community(testResult, [-1,  2], [0, 1, 2], True)
	expect_all_same_community(testResult, [ 1, -2], [0, 1, 2], True)
	expect_all_same_community(testResult, [10, 20], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [10, 15], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [15, 25], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [24, 25], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [25, 25], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [ 9, 10], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [10, 11], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [ 9, 11], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [ 9,-10], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [10,-11], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [ 9,-11], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [19, 20], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [20, 21], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [19, 21], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [19,-20], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [20,-21], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [19,-21], [0, 10, 20, 30, 40], False)

	expect_all_same_community(testResult, [10, 20, 30], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [10, 11, 12], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [10, 20, 11, 12, 13, 14, 15, 16, 17, 18, 19], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [10, 11, 12, 13, 20, 14, 15, 16, 17, 18, 19], [0, 10, 20, 30, 40], False)

	return testResult.result_str()

def test_get_k_lits():
	def expect_get_k_lits(testResult, temp_clause, k, cumulative_vec):
		# Since this function makes use of randomness, we just check invariants
		prev_size = len(temp_clause)
		clause = generate_random_degree_distribution.get_k_lits(temp_clause, k, cumulative_vec)

		# Check size of input
		testResult += expect(testResult, len(temp_clause), prev_size)

		# Check number of variables
		clause_vars = set([abs(l) for l in clause])
		testResult += expect(testResult, len(clause), k)
		testResult += expect(testResult, len(clause_vars), k)

		# Check that all variables are non-zero
		non_zero = any(l == 0 for l in clause)
		if non_zero:
			testResult += TEST_FAIL
			print("Test {} failed: received {}; expected non-zero variables".format(testResult.totalNumTests, clause))
		else: testResult += TEST_OKAY

		# Check that the largest generated variable falls within expected range
		largest_var = max(abs(l) for l in clause)
		if largest_var > len(cumulative_vec):
			testResult += TEST_FAIL
			print("Test {} failed: <actual> = <{}>; expected <= {}".format(testResult.totalNumTests, largest_var, len(cumulative_vec)))
		else: testResult += TEST_OKAY
	
	testResult = TestResult()

	expect_get_k_lits(testResult, [ ], 3, [10, 20, 30, 40])
	expect_get_k_lits(testResult, [ ], 4, [10, 20, 30, 40])
	expect_get_k_lits(testResult, [ ], 5, [10, 20, 30, 40])
	expect_get_k_lits(testResult, [1], 3, [10, 20, 30, 40])
	expect_get_k_lits(testResult, [1], 4, [10, 20, 30, 40])
	expect_get_k_lits(testResult, [1], 5, [10, 20, 30, 40])

	return testResult.result_str()

def test_generateRandomFormula():
	def expect_generateRandomFormula(testResult, n, m, k, cumulative_vec):
		# Since this function makes use of randomness, we just check invariants
		cnf = generate_random_degree_distribution.generateRandomFormula(n, m, k, cumulative_vec)

		# Check number of clauses
		testResult += expect(testResult, len(cnf), m)

		# Check sizes of clauses
		success = True
		for clause in cnf:
			if len(clause) != k:
				testResult += expect(testResult, len(clause), k)
				success = False
				break
		if success: testResult += TEST_OKAY

		# Check that the largest generated variable falls within expected range
		largest_var = max(max(abs(l) for l in c) for c in cnf)
		if largest_var > n:
			testResult += TEST_FAIL
			print("Test {} failed: <actual> = <{}>; expected <= {}".format(testResult.totalNumTests, largest_var, n))
		else: testResult += TEST_OKAY

	testResult = TestResult()

	expect_generateRandomFormula(testResult, 40,   0, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,   1, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,   2, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,   3, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,   4, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,   5, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,  10, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,  20, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,  30, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,  40, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40,  80, 3, [10, 20, 30, 40])
	expect_generateRandomFormula(testResult, 40, 160, 3, [10, 20, 30, 40])

	return testResult.result_str()

def test_generateRandomInterFormula():
	def expect_generateRandomInterFormula(testResult, community_id_upper_bounds, cvr, k, cnf, inter_vars):
		# Since this function makes use of randomness, we just check invariants
		prev_size = len(cnf)
		cnf = generate_random_degree_distribution.generateRandomInterFormula(community_id_upper_bounds, cvr, k, cnf, inter_vars)
		inter_cnf = cnf[prev_size:]

		# Check number of inter-community variables
		n = len(set([abs(l) for c in clause for l in c]))
		degree = len(community_id_upper_bounds) - 1
		testResult += expect(testResult, n, degree * (inter_vars // degree))

		# Check that the largest generated variable falls within expected range
		largest_var = max(max(abs(l) for l in c) for c in clause)
		if largest_var > community_id_upper_bounds[-1]:
			testResult += TEST_FAIL
			print("Test {} failed: <actual> = <{}>; expected <= {}".format(testResult.totalNumTests, largest_var, community_id_upper_bounds[-1]))
		else: testResult += TEST_OKAY

		# Check number of inter-community clauses
		m = int(n * cvr)
		testResult += expect(testResult, m, len(inter_cnf))

		# Check sizes of clauses
		success = True
		for clause in inter_cnf:
			if len(clause) != k:
				testResult += expect(testResult, len(clause), k)
				success = False
				break
		if success: testResult += TEST_OKAY

	testResult = TestResult()

	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 3, [   ], 4)
	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 3, [[1]], 4)
	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 3, [[1], [2, 3, 4]], 4)
	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 4, [   ], 4)
	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 4, [[1]], 4)
	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 4, [[1], [2, 3, 4]], 4)
	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 3, [   ], 5)
	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 3, [[1]], 5)
	expect_generateRandomInterFormula(testResult, [0, 10, 20, 30, 40, 50], 4., 3, [[1], [2, 3, 4]], 5)

	return testResult.result_str()

if __name__ == "__main__":
	print("test_get_n:                                   " + test_get_n())
	print("test_combine_subcnfs:                         " + test_combine_subcnfs())
	print("test_add_edges_to_combined_disconnected_cnfs: " + test_add_edges_to_combined_disconnected_cnfs())
	print("test_generateUniformVec:                      " + test_generateUniformVec())
	print("test_generatePowerlawVec:                     " + test_generatePowerlawVec())
	print("test_generateCumulative:                      " + test_generateCumulative())
	print("test_same_community:                          " + test_same_community())
	print("test_all_same_community:                      " + test_all_same_community())
	print("test_get_k_lits:                              " + test_get_k_lits())
	print("test_generateRandomFormula:                   " + test_generateRandomFormula())
	print("test_generateRandomInterFormula:              " + test_generateRandomInterFormula())