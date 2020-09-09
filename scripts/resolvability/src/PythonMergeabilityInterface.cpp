#include "PythonMergeabilityInterface.h"
#include <algorithm>
#include <cmath>
#include "paramComputation.h"
#include "mergeabilityCommon.h"

// PUBLIC

void PythonMergeabilityInterface::initializeClauses(long long* pyClauses, long long size) {
	// Reset previous values
	m_numVariables = 0;
	m_dirtyLookupTable = true;
	m_clauses.clear();

	// Read and store input
	_convertPyClausesToCpp(pyClauses, size);
}

void PythonMergeabilityInterface::calculateMergeabilityScore(long long* pyVarSet) {
	// Generate variable->clause lookup table
	if (m_dirtyLookupTable) _generateLookupTable();

	// Read variable set
	std::set<long long> varSet;
	_convertPyVarSetToCpp(varSet, pyVarSet);

	// Filter clauses by variable set
	std::vector<std::vector<unsigned int>> posClauseIndices(m_numVariables);
	std::vector<std::vector<unsigned int>> negClauseIndices(m_numVariables);
	_getLookupTablesForVarSet(posClauseIndices, negClauseIndices, varSet);

	// Calculate mergeability over the acceptable clauses
	m_output.mergeabilityScoreVector = std::vector<long long>(MSV_NUM_BUCKETS + 1);
	m_output.mergeabilityVector = std::vector<long long>(m_numVariables);

	ParamComputation::computeResolvable(&m_output, m_clauses, posClauseIndices, negClauseIndices);
}

double PythonMergeabilityInterface::getMergeabilityScoreNorm1() {
	return m_output.mergeabilityScore1 / static_cast<double>(m_output.totalNumResolvable);
}

double PythonMergeabilityInterface::getMergeabilityScoreNorm2() {
	const double m = static_cast<double>(m_clauses.size());
	return m_output.mergeabilityScore1 / (m * m);
}

// PRIVATE

void PythonMergeabilityInterface::_convertPyClausesToCpp(long long* pyClauses, long long size) {
	long long i = 0;
	while (i < size) {
		std::vector<long long> cppClause;
		while (pyClauses[i] != 0) {
			cppClause.push_back(pyClauses[i]);
			const long long var = std::abs(pyClauses[i]);
			m_numVariables = std::max(m_numVariables, var);
			++i;
		}
		++i;
		m_clauses.push_back(cppClause);
	}
}

void PythonMergeabilityInterface::_convertPyVarSetToCpp(std::set<long long>& varSet, long long* pyVarSet) {
	for (long long i = 0; pyVarSet[i] != 0; ++i) {
		const long long var = std::abs(pyVarSet[i]);
		// Filter out variables which do not appear in a clause (this should never happen, but just in case)
		if (m_posClauseIndices[var - 1].size() == 0 && m_negClauseIndices[var - 1].size() == 0) continue;
		varSet.emplace(var);
	}
}

void PythonMergeabilityInterface::_generateLookupTable() {
	// Allocate memory
	m_posClauseIndices = std::vector<std::vector<unsigned int>>(m_numVariables);
	m_negClauseIndices = std::vector<std::vector<unsigned int>>(m_numVariables);

	// Generate the lookup tables
	ParamComputation::computeLiteralClauseLookupTable(m_posClauseIndices, m_negClauseIndices, m_clauses);

	// Set state flag
	m_dirtyLookupTable = false;
}

void PythonMergeabilityInterface::_getLookupTablesForVarSet (
	std::vector<std::vector<unsigned int>>& posClauseIndices, std::vector<std::vector<unsigned int>>& negClauseIndices,
	const std::set<long long>& varSet
) {
	for (unsigned int i = 0; i < m_clauses.size(); ++i) {
		// Find clauses which contain variables outside of the variable set
		bool clauseContainsOtherVars = false;
		for (unsigned int j = 0; j < m_clauses[i].size(); ++j) {
			if (varSet.find(std::abs(m_clauses[i][j])) == varSet.end()) {
				clauseContainsOtherVars = true;
				break;
			}
		}

		// Add to the lookup table if the clause is acceptable
		if (!clauseContainsOtherVars) {
			for (unsigned int j = 0; j < m_clauses[i].size(); ++j) {
				const int var = m_clauses[i][j];
				if (var > 0) { // The variable should never be zero
					posClauseIndices[+var - 1].emplace_back(i);	
				} else {
					negClauseIndices[-var - 1].emplace_back(i);
				}
			}
		}
	}
}