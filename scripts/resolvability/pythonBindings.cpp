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

	void PMI_calculateMergeability(PythonMergeabilityInterface* interface, long long* varSet) {
		interface->calculateMergeabilityScore(varSet);
	}

	// Get mergeability score normalized by the total number of resolvable clauses
	double PMI_getMergeabilityScoreNorm1(PythonMergeabilityInterface* interface) {
		return interface->getMergeabilityScoreNorm1();
	}

	// Get mergeability score normalized by m^2
	double PMI_getMergeabilityScoreNorm1(PythonMergeabilityInterface* interface) {
		return interface->getMergeabilityScoreNorm2();
	}
}
