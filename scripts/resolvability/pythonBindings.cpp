#include <Python.h>
#include <iostream>
#include <set>
#include <vector>
#include "src/paramComputation.h"
#include "src/PythonMergeabilityInterface.h"

extern "C" {
	PythonMergeabilityInterface* PMI_init() {
		return new PythonMergeabilityInterface();
	}

	void PMI_destroy(PythonMergeabilityInterface* interface) {
		delete interface;
	}

	void PMI_setClauses(PythonMergeabilityInterface* interface, long long* pyClauses, long long size) {
		interface->initializeClauses(pyClauses, size);
	}

	long long PMI_calculateMergeability(PythonMergeabilityInterface* interface, long long* varSet) {
		return interface->calculateMergeability(varSet);
	}
}
