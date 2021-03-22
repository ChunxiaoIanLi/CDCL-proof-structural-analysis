import HCS_to_CNF_direct
import generate_random_degree_distribution
from decimal import Decimal

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
		level, depth, offset, degree_vector, inter_vars_fraction, community_id_upper_bounds, k, cnf,
		expected_num_inter_vars, cvr
	):
		# Since this function makes use of randomness, we just check graph invariants
		num_original_clauses = len(cnf)
		cnf = HCS_to_CNF_direct.add_edges_to_combined_disconnected_cnfs(level, depth, offset, degree_vector, inter_vars_fraction, community_id_upper_bounds, k, cnf, cvr)
		
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
	cnf = [[1, 2, 3], [-1, -2, 3], [2, 3], [4, 5, 6], [-4, 5, -6], [7, 8, 9], [10, -11, -12], [-8, 9, 11]]
	n = max(abs(l) for c in cnf for l in c)
	degree_vector = [0] * n
	for c in cnf:
		for l in c: degree_vector[abs(l) - 1] += 1

	expect_add_edges_to_combined_disconnected_cnfs(testResult, 1, 1, 0, degree_vector, 1/3., [0, 6, 12], 3, cnf[:], 4, [1.])
	expect_add_edges_to_combined_disconnected_cnfs(testResult, 1, 1, 0, degree_vector, 1/2., [0, 6, 12], 3, cnf[:], 6, [1.])
	expect_add_edges_to_combined_disconnected_cnfs(testResult, 1, 1, 0, degree_vector, 1/3., [0, 6, 12], 4, cnf[:], 4, [1.])
	expect_add_edges_to_combined_disconnected_cnfs(testResult, 1, 1, 0, degree_vector, 1/2., [0, 6, 12], 4, cnf[:], 6, [1.])

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

def test_all_same_community():
	def expect_all_same_community(testResult, literals, community_id_upper_bounds, expectation):
		testResult += expect(testResult, generate_random_degree_distribution.all_same_community(literals, community_id_upper_bounds), expectation)

	testResult = TestResult()

	expect_all_same_community(testResult, [ 1,  1], [0, 1], True)
	expect_all_same_community(testResult, [-1,  1], [0, 1], True)
	expect_all_same_community(testResult, [ 1,  1], [0, 2], True)
	expect_all_same_community(testResult, [-1,  1], [0, 2], True)
	expect_all_same_community(testResult, [ 1,  2], [0, 1, 2], False)
	expect_all_same_community(testResult, [-1,  2], [0, 1, 2], False)
	expect_all_same_community(testResult, [ 1, -2], [0, 1, 2], False)
	expect_all_same_community(testResult, [10, 20], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [10, 15], [0, 10, 20, 30, 40], False)
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
	expect_all_same_community(testResult, [11, 12, 13], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [11, 12, 13, 14, 15, 16, 17, 18, 19, 20], [0, 10, 20, 30, 40], True)
	expect_all_same_community(testResult, [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 10], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], [0, 10, 20, 30, 40], False)
	expect_all_same_community(testResult, [11, 12, 13, 10, 14, 15, 16, 17, 18, 19, 20], [0, 10, 20, 30, 40], False)

	return testResult.result_str()

def choose(n, k):
	"""
	A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
	https://stackoverflow.com/questions/3025162/statistics-combinations-in-python
	"""
	if 0 <= k <= n:
		ntok = 1
		ktok = 1
		for t in range(1, min(k, n - k) + 1):
			ntok *= n
			ktok *= t
			n -= 1
		return ntok // ktok
	else:
		print(k, n)
		return 0

def expect_polarity_distribution(testResult, lits):
	# Check probability of this polarity distribution
	# P = choose(total, num_negative) * (chance_negative)^(num_negative) * (chance_non_negative)^(num_non_negative)
	expected_negation_fraction = 0.5
	num_negative = sum(int(l) < 0 for l in lits)
	actual_probability = choose(len(lits), num_negative) * Decimal(expected_negation_fraction)**(num_negative) * (1 - Decimal(expected_negation_fraction))**(len(lits) - num_negative)

	# Calculate probability of the expected polarity distribution
	expected_num_negative = int(len(lits) * expected_negation_fraction)
	expected_probability = choose(len(lits), expected_num_negative) * Decimal(expected_negation_fraction)**(expected_num_negative) * (1 - Decimal(expected_negation_fraction))**(len(lits) - expected_num_negative)

	# If the chance of this distribution is less than 0.1% of the probability of the expected distribution, raise an error
	min_chance = 0.001
	if actual_probability / expected_probability < min_chance:
		testResult += TEST_FAIL
		print("Test {} failed: probability of polarity distribution = <{}>; expected >= {}".format(testResult.totalNumTests, actual_probability, expected_probability))
		print("Received polarity distribution <+,-> = <{}, {}>".format(len(lits) - num_negative, num_negative))
	else: testResult += TEST_OKAY

def expect_degree_distribution(testResult, lits, input_degree_vector):
	# Initialize degree vectors
	total_original_degree = sum(abs(degree) for degree in input_degree_vector)
	actual_degree_vector = [0] * len(input_degree_vector)
	for l in lits: actual_degree_vector[abs(l) - 1] += 1
	total_actual_degree = sum(abs(degree) for degree in actual_degree_vector)
	scaling = total_actual_degree / total_original_degree
	input_degree_vector = [scaling * degree for degree in input_degree_vector]

	# Calculate distance from expectation
	distance = sum(abs(actual_degree_vector[i] - input_degree_vector[i]) for i in range(len(input_degree_vector)))
	avg_dist = distance / len(input_degree_vector)

	# If the chance of this distribution is less than 0.1% of the probability of the expected distribution, raise an error
	min_dist = sum(deg**0.5 for deg in input_degree_vector)
	if avg_dist > min_dist:
		testResult += TEST_FAIL
		print("Test {} failed: avg. distance = <{}>; expected <= <{}>".format(testResult.totalNumTests, avg_dist, min_dist))
		print("Received degree distribution: {}; expected: {}".format(actual_degree_vector, input_degree_vector))
	else: testResult += TEST_OKAY

def test_get_k_lits():
	def expect_get_k_lits(testResult, temp_clause, k, degree_vec):
		# Since this function makes use of randomness, we just check invariants
		clause = generate_random_degree_distribution.get_k_lits(temp_clause, k, degree_vec)

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
		if largest_var > len(degree_vec):
			testResult += TEST_FAIL
			print("Test {} failed: <actual> = <{}>; expected <= {}".format(testResult.totalNumTests, largest_var, len(degree_vec)))
		else: testResult += TEST_OKAY

		# Check probability of this polarity distribution
		expect_polarity_distribution(testResult, clause)

	testResult = TestResult()

	expect_get_k_lits(testResult, [ ], 3, [10, 10, 10, 10, 10])
	expect_get_k_lits(testResult, [ ], 4, [10, 10, 10, 10, 10])
	expect_get_k_lits(testResult, [ ], 5, [10, 10, 10, 10, 10])
	expect_get_k_lits(testResult, [ ], 5, [10,  5,  2,  1,  1])
	expect_get_k_lits(testResult, [1], 3, [10, 10, 10, 10, 10])
	expect_get_k_lits(testResult, [1], 4, [10, 10, 10, 10, 10])
	expect_get_k_lits(testResult, [1], 5, [10, 10, 10, 10, 10])
	expect_get_k_lits(testResult, [1], 5, [10,  5,  2,  1,  1])

	expect_get_k_lits(testResult, [1], 500, [1] * 500)

	return testResult.result_str()

def test_select_from_random_communities():
	testResult = TestResult()

	# Check that the function generates all combinations of clauses
	num_vars = 2
	expected_num_clauses = 2**num_vars
	num_tests = 10
	for i in range(num_tests):
		cnf = []
		while len(cnf) < expected_num_clauses:
			while True:
				tmp_clause = generate_random_degree_distribution.select_from_random_communities([], [1] * num_vars, range(1, num_vars + 1), num_vars, range(0, num_vars + 1))
				if tmp_clause not in cnf: break
			cnf.append(tmp_clause)
	
		# Check number of clauses
		testResult += expect(testResult, len(cnf), expected_num_clauses)

	return testResult.result_str()

def test_select_inter_vars():
	testResult = TestResult()

	# Check that the function generates all combinations of clauses
	num_vars = 2
	expected_num_clauses = 2**num_vars
	num_tests = 10
	for i in range(num_tests):
		cnf = []
		while len(cnf) < expected_num_clauses:
			cnf.append(generate_random_degree_distribution.select_inter_vars(cnf, [], [1] * num_vars, range(1, num_vars + 1), num_vars, range(0, num_vars + 1)))

		# Check number of clauses
		testResult += expect(testResult, len(cnf), expected_num_clauses)

	# Check that the function generates the expected distribution
	num_vars = 1000
	lits = generate_random_degree_distribution.select_inter_vars([], [], [1] * num_vars, range(1, num_vars + 1), num_vars, range(0, num_vars + 1))
	expect_polarity_distribution(testResult, lits)

	return testResult.result_str()

def test_generateRandomFormula():
	def expect_generateRandomFormula(testResult, n, m, k, degree_vec):
		# Since this function makes use of randomness, we just check invariants
		cnf = generate_random_degree_distribution.generateRandomFormula(n, m, k, degree_vec)

		# Check number of clauses
		testResult += expect(testResult, len(cnf), m)

		# Check sizes of clauses
		success = True
		for clause in cnf:
			if len(clause) != k:
				testResult += expect(testResult, len(clause), k)
				success = False
				break
			
			# Check for duplicate variables
			var_set = set(abs(l) for l in clause)
			if len(var_set) != k:
				testResult += expect(testResult, len(var_set), k)
				success = False
				break
		if success: testResult += TEST_OKAY

		# Check that the largest generated variable falls within expected range
		largest_var = max(max(abs(l) for l in c) for c in [[0]] + cnf)
		if largest_var > n:
			testResult += TEST_FAIL
			print("Test {} failed: <actual> = <{}>; expected <= {}".format(testResult.totalNumTests, largest_var, n))
		else: testResult += TEST_OKAY

		# Check probability of this distribution
		lits = [l for c in cnf for l in c]
		expect_polarity_distribution(testResult, lits)
		expect_degree_distribution(testResult, lits, degree_vec)

	testResult = TestResult()

	expect_generateRandomFormula(testResult, 7,  3, 3, [ 2,  2,  1,  1,  1,  1,  1])
	expect_generateRandomFormula(testResult, 7,  4, 3, [ 2,  2,  2,  2,  2,  1,  1])
	expect_generateRandomFormula(testResult, 7,  5, 3, [ 3,  2,  2,  1,  3,  2,  2])
	expect_generateRandomFormula(testResult, 7, 10, 3, [ 5,  5,  4,  4,  4,  4,  4])
	expect_generateRandomFormula(testResult, 7, 20, 3, [ 9,  9,  9,  9,  8,  8,  8])
	expect_generateRandomFormula(testResult, 7, 30, 3, [13, 13, 13, 13, 13, 13, 12])
	expect_generateRandomFormula(testResult, 7, 30, 3, [25, 21, 18, 13,  9,  3,  1])
	expect_generateRandomFormula(testResult, 7, 25, 2, [16, 12,  8,  6,  4,  2,  2])
	
	expect_generateRandomFormula(testResult, 100, 500, 3, [1] * 100)

	return testResult.result_str()

def test_generateRandomInterFormula():
	def expect_generateRandomInterFormula(testResult, offset, degree_vector, community_id_upper_bounds, cvr, k, cnf, inter_vars):
		# Since this function makes use of randomness, we just check invariants
		prev_size = len(cnf)
		cnf = generate_random_degree_distribution.generateRandomInterFormula(offset, degree_vector, community_id_upper_bounds, cvr, k, cnf, inter_vars)
		inter_cnf = cnf[prev_size:]

		# Check number of inter-community variables
		n = len(set([abs(l) for c in inter_cnf for l in c]))
		degree = len(community_id_upper_bounds) - 1
		testResult += expect(testResult, n, degree * (inter_vars // degree))

		# Check that the largest generated variable falls within expected range
		largest_var = max(max(abs(l) for l in c) for c in [[0]] + inter_cnf)
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
			# Check size of clause
			if len(clause) != k:
				testResult += expect(testResult, len(clause), k)
				success = False
				break

			# Check for duplicate variables
			var_set = set(abs(l) for l in clause)
			if len(var_set) != k:
				testResult += expect(testResult, len(var_set), k)
				success = False
				break
			
		if success: testResult += TEST_OKAY

		# Check probability of this distribution
		lits = [l for c in inter_cnf for l in c]
		actual_degree_vector = [0] * len(degree_vector)
		for l in lits: actual_degree_vector[abs(l) - 1] += 1
		expected_degree_vector = [degree_vector[i] if deg else 0 for i, deg in enumerate(actual_degree_vector)]
		expect_polarity_distribution(testResult, lits)
		expect_degree_distribution(testResult, lits, expected_degree_vector)

	testResult = TestResult()

	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 3, [   ], 4)
	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 3, [[1]], 4)
	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 3, [[1], [2, 3, 4]], 4)
	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 4, [   ], 4)
	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 4, [[1]], 4)
	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 4, [[1], [2, 3, 4]], 4)
	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 3, [   ], 5)
	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 3, [[1]], 5)
	expect_generateRandomInterFormula(testResult, 0, [1] * 20, [0, 10, 20], 3., 3, [[1], [2, 3, 4]], 5)
	
	expect_generateRandomInterFormula(testResult, 0, [1] * 500, [0, 250, 500], 3., 3, [[1], [2, 3, 4]], 5)

	return testResult.result_str()

def test_generate_VIG():
	def expect_generate_VIG(depth, leaf_community_size, inter_vars_fraction, degree, k, cvr):
		# Generate CNF with uniform degree vector
		n = leaf_community_size * degree**(depth - 1)
		degree_vector = [1] * n
		cnf = HCS_to_CNF_direct.generate_VIG(1, depth, 0, degree_vector, leaf_community_size, inter_vars_fraction, [degree] * (depth - 1), k, cvr)

		# Check probability of this distribution
		lits = [l for c in cnf for l in c]
		actual_degree_vector = [0] * len(degree_vector)
		for l in lits: actual_degree_vector[abs(l) - 1] += 1
		expect_polarity_distribution(testResult, lits)
		expected_degree_vector = [degree_vector[i] if deg else 0 for i, deg in enumerate(actual_degree_vector)]
		expect_degree_distribution(testResult, lits, expected_degree_vector)

		# Generate CNF with non-uniform degree vector
		n = leaf_community_size * degree**(depth - 1)
		degree_vector = [1] * n
		degree_vector[0] = leaf_community_size
		cnf = HCS_to_CNF_direct.generate_VIG(1, depth, 0, degree_vector, leaf_community_size, inter_vars_fraction, [degree] * (depth - 1), k, cvr)

		# Check probability of this distribution
		lits = [l for c in cnf for l in c]
		actual_degree_vector = [0] * len(degree_vector)
		for l in lits: actual_degree_vector[abs(l) - 1] += 1
		expect_polarity_distribution(testResult, lits)
		expected_degree_vector = [degree_vector[i] if deg else 0 for i, deg in enumerate(actual_degree_vector)]
		expect_degree_distribution(testResult, lits, expected_degree_vector)

		# Generate CNF with non-uniform degree vector
		n = leaf_community_size * degree**(depth - 1)
		degree_vector = range(1, n + 1)
		cnf = HCS_to_CNF_direct.generate_VIG(1, depth, 0, degree_vector, leaf_community_size, inter_vars_fraction, [degree] * (depth - 1), k, cvr)

		# Check probability of this distribution
		lits = [l for c in cnf for l in c]
		actual_degree_vector = [0] * len(degree_vector)
		for l in lits: actual_degree_vector[abs(l) - 1] += 1
		expect_polarity_distribution(testResult, lits)
		expected_degree_vector = [degree_vector[i] if deg else 0 for i, deg in enumerate(actual_degree_vector)]
		expect_degree_distribution(testResult, lits, expected_degree_vector)

	testResult = TestResult()

	expect_generate_VIG(1, 10, 0.0, 2, 3, [4.0])
	expect_generate_VIG(2, 10, 0.0, 2, 3, [3.5, 4.0])
	expect_generate_VIG(3, 10, 0.0, 2, 3, [3.0, 3.5, 4.0])

	expect_generate_VIG(1, 10, 0.2, 2, 3, [4.0])
	expect_generate_VIG(2, 10, 0.2, 2, 3, [3.5, 4.0])
	expect_generate_VIG(3, 10, 0.2, 2, 3, [3.0, 3.5, 4.0])

	expect_generate_VIG(1, 50, 0.3, 4, 3, [4.0])
	expect_generate_VIG(2, 50, 0.3, 4, 3, [3.5, 4.0])
	expect_generate_VIG(3, 50, 0.3, 4, 3, [3.0, 3.5, 4.0])
	
	return testResult.result_str()

if __name__ == "__main__":
	print("test_combine_subcnfs:                         " + test_combine_subcnfs())
	print("test_add_edges_to_combined_disconnected_cnfs: " + test_add_edges_to_combined_disconnected_cnfs())
	print("test_generateUniformVec:                      " + test_generateUniformVec())
	print("test_generatePowerlawVec:                     " + test_generatePowerlawVec())
	print("test_all_same_community:                      " + test_all_same_community())
	print("test_get_k_lits:                              " + test_get_k_lits())
	print("test_select_from_random_communities:          " + test_select_from_random_communities())
	print("test_select_inter_vars:                       " + test_select_inter_vars())
	print("test_generateRandomFormula:                   " + test_generateRandomFormula())
	print("test_generateRandomInterFormula:              " + test_generateRandomInterFormula())
	print("test_generate_VIG:                            " + test_generate_VIG())