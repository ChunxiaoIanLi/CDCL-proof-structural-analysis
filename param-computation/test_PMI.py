from PMILib import PMI
from cnf_to_edge_set import read_file, cnf_to_clauses_list
import math

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

# Create object
pmi = PMI()

def test_merge_res_expect(testResult, clauses, varset, expectedMergeability, expectedResolvability, mode = 0):
	# Load clauses
	clause_list = cnf_to_clauses_list(clauses)
	pmi.setClauses(clause_list)
	varset.append(0)

	# Calculate stats
	pmi.calculate(varset, mode)
	resolvability = pmi.getResolvability()
	mergeability = pmi.getMergeability()
	if (expectedMergeability != mergeability) or (expectedResolvability != resolvability):
		testResult += TEST_FAIL
		print("Test {} failed: actual <m,r> = <{},{}>; expected <m,r> = <{},{}>".format(testResult.totalNumTests, mergeability, resolvability, expectedMergeability, expectedResolvability))
	else: testResult += TEST_OKAY

def test_basic_merge_res():
	def test_basic_merge_res_expect(testResult, index, expectedMergeability, expectedResolvability):
		# Load clauses from file
		clauses, m, n = read_file("mergeability_test_suite/{}.cnf".format(index))
		varset = range(1, n + 1)
		return test_merge_res_expect(testResult, clauses, varset, expectedMergeability, expectedResolvability)

	testResult = TestResult(0, 0)

	# Check basic test cases
	test_merge_res_expect(testResult, [                  ], [    ], 0, 0, 0)
	test_merge_res_expect(testResult, [[+1    ], [+1    ]], [1   ], 0, 0, 0)
	test_merge_res_expect(testResult, [[+1    ], [-1    ]], [1   ], 0, 1, 0)
	test_merge_res_expect(testResult, [[+1, +2], [+1, +2]], [1, 2], 0, 0, 0)
	test_merge_res_expect(testResult, [[+1, +2], [+1, -2]], [1, 2], 1, 1, 0)
	test_merge_res_expect(testResult, [[+1, +2], [-1, +2]], [1, 2], 1, 1, 0)
	test_merge_res_expect(testResult, [[+1, +2], [-1, -2]], [1, 2], 0, 0, 0)

	# Check testcases from file
	test_basic_merge_res_expect(testResult,  1,  0,  0)
	test_basic_merge_res_expect(testResult,  2,  0,  3)
	test_basic_merge_res_expect(testResult,  3,  0,  2)
	test_basic_merge_res_expect(testResult,  4,  0, 10)
	test_basic_merge_res_expect(testResult,  5,  0, 10)
	test_basic_merge_res_expect(testResult,  6,  0, 19)
	test_basic_merge_res_expect(testResult,  7,  5,  5)
	test_basic_merge_res_expect(testResult,  8,  5,  5)
	test_basic_merge_res_expect(testResult,  9, 10, 10)
	test_basic_merge_res_expect(testResult, 10, 10, 10)
	test_basic_merge_res_expect(testResult, 11,  5, 10)
	test_basic_merge_res_expect(testResult, 12,  5, 10)
	test_basic_merge_res_expect(testResult, 13,  5, 19)
	test_basic_merge_res_expect(testResult, 14, 19, 19)
	test_basic_merge_res_expect(testResult, 15,  0,  9)
	test_basic_merge_res_expect(testResult, 16,  4,  9)
	test_basic_merge_res_expect(testResult, 17,  2,  9)
	test_basic_merge_res_expect(testResult, 18,  5, 10)
	test_basic_merge_res_expect(testResult, 19,  0, 10)
	test_basic_merge_res_expect(testResult, 20,  5,  5)
	test_basic_merge_res_expect(testResult, 21,  4, 11)
	test_basic_merge_res_expect(testResult, 22,  5, 10)
	test_basic_merge_res_expect(testResult, 23, 19, 19)

	return testResult.result_str()

def test_mergeability_scores():
	def test_mergeability_scores_expect(testResult, clauses, expected_ms1n1, expected_ms1n2, expected_ms2n1, expected_ms2n2):
		# Load clauses
		clause_list = cnf_to_clauses_list(clauses)
		pmi.setClauses(clause_list)
		varset = range(1, max(abs(l) for c in clauses for l in c) + 1) + [0] if clauses else [0]

		# Calculate stats
		mode = 0
		pmi.calculate(varset, mode)
		ms1n1 = pmi.getMergeabilityScore1Norm1()
		ms1n2 = pmi.getMergeabilityScore1Norm2()
		ms2n1 = pmi.getMergeabilityScore2Norm1()
		ms2n2 = pmi.getMergeabilityScore2Norm2()

		if ms1n1 != expected_ms1n1 and not(math.isnan(ms1n1) and math.isnan(expected_ms1n1)):
			testResult += TEST_FAIL
			print("Test {} failed: actual <ms1n1> = <{}>; expected <ms1n1> = <{}>".format(testResult.totalNumTests, ms1n1, expected_ms1n1))
		elif ms1n2 != expected_ms1n2 and not(math.isnan(ms1n2) and math.isnan(expected_ms1n2)):
			testResult += TEST_FAIL
			print("Test {} failed: actual <ms1n2> = <{}>; expected <ms1n2> = <{}>".format(testResult.totalNumTests, ms1n2, expected_ms1n2))
		elif ms2n1 != expected_ms2n1 and not(math.isnan(ms2n1) and math.isnan(expected_ms2n1)):
			testResult += TEST_FAIL
			print("Test {} failed: actual <ms2n1> = <{}>; expected <ms2n1> = <{}>".format(testResult.totalNumTests, ms2n1, expected_ms2n1))
		elif ms2n2 != expected_ms2n2 and not(math.isnan(ms2n2) and math.isnan(expected_ms2n2)):
			testResult += TEST_FAIL
			print("Test {} failed: actual <ms2n2> = <{}>; expected <ms2n2> = <{}>".format(testResult.totalNumTests, ms2n2, expected_ms2n2))
		else: testResult += TEST_OKAY

	testResult = TestResult(0, 0)

	# Test computation of mergeability scores
	nan = float('nan')
	test_mergeability_scores_expect(testResult, [                     ],   nan,   nan,  nan,   nan)
	test_mergeability_scores_expect(testResult, [[1, 2   ], [-1, -2   ]],  nan,   0.0,  nan,   0.0)
	test_mergeability_scores_expect(testResult, [[1, 2, 3], [-1, -2, 3]],  nan,   0.0,  nan,   0.0)
	test_mergeability_scores_expect(testResult, [[1, 2   ], [-1,  3   ]],  0.0,   0.0,  0.0,   0.0)
	test_mergeability_scores_expect(testResult, [[1, 2   ], [-1,  2   ]], 1./2, 1./ 8, 1./1, 1./ 4)
	test_mergeability_scores_expect(testResult, [[1, 2, 3], [-1,  2, 3]], 1./2, 1./ 8, 1./1, 1./ 4)
	test_mergeability_scores_expect(testResult, [[1, 2, 3], [-1,  2, 4]], 1./4, 1./16, 1./3, 1./12)

	return testResult.result_str()

def test_var_set():
	testResult = TestResult(0, 0)

	# Test clause inclusion/exclusion
	clauses = [[1, 2, 3], [-1, 2, 3]]
	test_merge_res_expect(testResult, clauses, [       ], 0, 0, 0)
	test_merge_res_expect(testResult, clauses, [       ], 0, 0, 1)
	test_merge_res_expect(testResult, clauses, [1      ], 0, 0, 0)
	test_merge_res_expect(testResult, clauses, [1      ], 0, 1, 1)
	test_merge_res_expect(testResult, clauses, [1, 2   ], 0, 0, 0)
	test_merge_res_expect(testResult, clauses, [1, 2   ], 1, 1, 1)
	test_merge_res_expect(testResult, clauses, [2, 3   ], 0, 0, 0)
	test_merge_res_expect(testResult, clauses, [2, 3   ], 0, 0, 1)
	test_merge_res_expect(testResult, clauses, [1, 2, 3], 2, 1, 0)
	test_merge_res_expect(testResult, clauses, [1, 2, 3], 2, 1, 1)
	clauses = [[1, 2, 3], [-1, 2, 3], [2, -3, 4]]
	test_merge_res_expect(testResult, clauses, [1, 2, 3], 2, 1, 0)
	test_merge_res_expect(testResult, clauses, [1, 2, 3], 4, 3, 1)
	test_merge_res_expect(testResult, clauses, [   2, 3], 0, 0, 0)
	test_merge_res_expect(testResult, clauses, [   2, 3], 2, 2, 1)

	return testResult.result_str()

def test_width():
	def test_width_expect(testResult, clauses, varset, expectedPreWidth, expectedPostWidth, mode = 0):
		# Load clauses
		clause_list = cnf_to_clauses_list(clauses)
		pmi.setClauses(clause_list)
		varset.append(0)

		# Calculate stats
		pmi.calculate(varset, mode)
		preWidth  = pmi.getPreResolutionClauseWidth()
		postWidth = pmi.getPostResolutionClauseWidth()
		if (expectedPreWidth != preWidth) or (expectedPostWidth != postWidth):
			testResult += TEST_FAIL
			print("Test {} failed: actual <pre,post> = <{},{}>; expected <pre,post> = <{},{}>".format(testResult.totalNumTests, preWidth, postWidth, expectedPreWidth, expectedPostWidth))
		else: testResult += TEST_OKAY

	testResult = TestResult(0, 0)

	test_width_expect(testResult, [                     ], [             ], 0.0, 0, 0)
	test_width_expect(testResult, [                     ], [             ], 0.0, 0, 1)
	test_width_expect(testResult, [[1, 2, 3], [-1, 2, 3]], [1, 2, 3      ], 3.0, 2, 0)
	test_width_expect(testResult, [[1, 2, 3], [-1, 2, 3]], [1, 2, 3      ], 3.0, 2, 1)
	test_width_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3      ], 3.0, 0, 0)
	test_width_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3      ], 2.0, 2, 1)
	test_width_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3, 4   ], 3.0, 0, 0)
	test_width_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3, 4   ], 2.5, 3, 1)
	test_width_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3, 4, 5], 3.0, 4, 0)
	test_width_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3, 4, 5], 3.0, 4, 1)

	return testResult.result_str()

def test_cvr():
	def test_cvr_expect(testResult, clauses, varset, expectedCVR, mode = 0):
		# Load clauses
		clause_list = cnf_to_clauses_list(clauses)
		pmi.setClauses(clause_list)
		varset.append(0)

		# Calculate stats
		pmi.calculate(varset, mode)
		cvr = pmi.getCVR()
		if expectedCVR != cvr and not (math.isnan(expectedCVR) and math.isnan(cvr)):
			testResult += TEST_FAIL
			print("Test {} failed: actual <cvr> = <{}>; expected <cvr> = <{}>".format(testResult.totalNumTests, cvr, expectedCVR))
		else: testResult += TEST_OKAY

	testResult = TestResult(0, 0)

	test_cvr_expect(testResult, [                     ], [                ], float("nan"), 0)
	test_cvr_expect(testResult, [                     ], [                ], float("nan"), 1)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 2, 3]], [1, 2, 3         ], 2/3., 0)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 2, 3]], [1, 2, 3         ], 2/3., 1)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3         ], 1/3., 0)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3         ], 2/3., 1)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1               ], float("nan"), 0)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1               ], 2/1., 1)
	test_cvr_expect(testResult, [[1, 2, 3], [ 4, 5, 6]], [1, 2, 3         ], 1/3., 0)
	test_cvr_expect(testResult, [[1, 2, 3], [ 4, 5, 6]], [1, 2, 3         ], 1/3., 1)
	test_cvr_expect(testResult, [[1, 2, 3], [ 4, 5, 6]], [      3, 4      ], float("nan"), 0)
	test_cvr_expect(testResult, [[1, 2, 3], [ 4, 5, 6]], [      3, 4      ], 2/2., 1)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3, 4, 5   ], 2/5., 0)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3, 4, 5   ], 2/5., 1)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3, 4, 5, 6], 2/5., 0)
	test_cvr_expect(testResult, [[1, 2, 3], [-1, 4, 5]], [1, 2, 3, 4, 5, 6], 2/5., 1)
	test_cvr_expect(testResult, [[1, 2, 3], [ 4, 5, 6]], [1, 2, 3, 4, 5, 6], 2/6., 0)
	test_cvr_expect(testResult, [[1, 2, 3], [ 4, 5, 6]], [1, 2, 3, 4, 5, 6], 2/6., 1)

	return testResult.result_str()

if __name__ == "__main__":
	print("test_basic_merge_res:     " + test_basic_merge_res())
	print("test_mergeability_scores: " + test_mergeability_scores())
	print("test_var_set:             " + test_var_set())
	print("test_width:               " + test_width())
	print("test_cvr:                 " + test_cvr())