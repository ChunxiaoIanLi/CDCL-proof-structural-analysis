import HCS_query

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

def expect_error(testResult, actual):
	print("Test {} failed: <actual> = <{}>; expected ERROR".format(testResult.totalNumTests, actual))
	return TEST_FAIL

def test_reconstruct_community_edges():
	def expect_reconstruct_community_edges(testResult, degree_stack, expected):
		testResult += expect(testResult, HCS_query.reconstruct_community_edges(degree_stack), expected)
	
	def expect_error_reconstruct_community_edges(testResult, degree_stack):
		try:    testResult += expect_error(testResult, HCS_query.reconstruct_community_edges(degree_stack))
		except: testResult += TEST_OKAY
	
	testResult = TestResult()

	# Check that the correct edges are assigned for valid data
	expect_reconstruct_community_edges(testResult, [], [])
	expect_reconstruct_community_edges(testResult, [1], [])
	expect_reconstruct_community_edges(testResult, [2, 1, 1], [
		(0, 1), (0, 2)
	])
	expect_reconstruct_community_edges(testResult, [2, 2, 1, 1, 1], [
		(0, 1), (0, 2),
		(1, 3), (1, 4)
	])
	expect_reconstruct_community_edges(testResult, [2, 2, 2, 1, 1, 1, 1], [
		(0, 1), (0, 2),
		(1, 3), (1, 4), (2, 5), (2, 6)
	])
	expect_reconstruct_community_edges(testResult, [3, 2, 2, 1, 1, 1, 1, 1], [
		(0, 1), (0, 2), (0, 3),
		(1, 4), (1, 5), (2, 6), (2, 7)
	])
	expect_reconstruct_community_edges(testResult, [2, 3, 2, 1, 1, 1, 1, 1], [
		(0, 1), (0, 2),
		(1, 3), (1, 4), (1, 5), (2, 6), (2, 7)
	])
	expect_reconstruct_community_edges(testResult, [2, 3, 2, 1, 1, 3, 1, 1, 1, 1, 1], [
		(0, 1), (0, 2),
		(1, 3), (1, 4), (1,  5), (2, 6), (2, 7),
		(5, 8), (5, 9), (5, 10)
	])

	# Check error detection
	expect_error_reconstruct_community_edges(testResult, [2])
	expect_error_reconstruct_community_edges(testResult, [2, 1])
	expect_error_reconstruct_community_edges(testResult, [1, 2, 1, 1])
	expect_error_reconstruct_community_edges(testResult, [2, 3, 2, 1, 1, 3, 1, 1, 1, 1])
	expect_error_reconstruct_community_edges(testResult, [2, 3, 2, 1, 1, 3, 2, 2, 1, 1])

	return testResult.result_str()

if __name__ == '__main__':
	print("test_reconstruct_community_edges: " + test_reconstruct_community_edges())