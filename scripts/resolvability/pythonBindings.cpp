#include <Python.h>
#include <iostream>
#include <vector>
#include "paramComputation.h"

static int convertPyClausesToCpp(std::vector<std::vector<long long>>& cppClauses, PyObject* pyClauses) {
	if (!PyList_Check(pyClauses)) return 1;
	for (Py_ssize_t i = 0; i < PyList_Size(pyClauses); ++i) {
		std::vector<long long> cppClause;
		PyObject* pyClause = PyList_GetItem(pyClauses, i);
		if (!PyList_Check(pyClause)) return 1;
		for (Py_ssize_t j = 0; j < PyList_Size(pyClause); ++j) {
			PyObject* pyLiteral = PyList_GetItem(pyClause, i);
			cppClause.push_back(PyLong_AsLongLong(pyLiteral));
		}
		cppClauses.push_back(cppClause);
	}

	return 0;
}

static PyObject* _calculateMergeability(PyObject* pyClauses, PyObject* pyNumVars) {
	const long long numVars = PyLong_AsLongLong(pyNumVars);
	std::vector<std::vector<long long>> cppClauses;
	if (convertPyClausesToCpp(cppClauses, pyClauses)) {
		std::cerr << "Error: input object is not a python list" << std::endl;
		return NULL;
	}

	long long totalNumResolvable = 0;
	long long totalNumMergeable = 0;
	ParamComputation::computeMergeability(totalNumResolvable, totalNumMergeable, cppClauses, numVars);
	return PyLong_FromLongLong(totalNumMergeable);
}

extern "C" {
	PyObject* calculateMergeability(PyObject* pyClauses, PyObject* pyNumVars) {
		return _calculateMergeability(pyClauses, pyNumVars);
	}
}