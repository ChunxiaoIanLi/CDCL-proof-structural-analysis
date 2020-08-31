#include <Python.h>
#include <iostream>
#include <vector>
#include "src/paramComputation.h"

static void convertPyClausesToCpp(std::vector<std::vector<long long>>& cppClauses, long long* pyClauses, long long size) {
	long long i = 0;
	while (i < size) {
		std::vector<long long> cppClause;
		while (pyClauses[i] != 0) {
			cppClause.push_back(pyClauses[i]);
			++i;
		}
		++i;
		cppClauses.push_back(cppClause);
	}
}

static long long _calculateMergeability(long long* pyClauses, long long numVars, long long size) {
	std::vector<std::vector<long long>> cppClauses;
	convertPyClausesToCpp(cppClauses, pyClauses, size);

	long long totalNumResolvable = 0;
	long long totalNumMergeable = 0;
	ParamComputation::computeMergeability(totalNumResolvable, totalNumMergeable, cppClauses, numVars);
	return totalNumMergeable;
}

extern "C" {
	long long calculateMergeability(long long* pyClauses, long long numVars, long long size) {
		return _calculateMergeability(pyClauses, numVars, size);
	}
}
