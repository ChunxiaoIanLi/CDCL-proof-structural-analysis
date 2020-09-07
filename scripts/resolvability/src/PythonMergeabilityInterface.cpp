#include "PythonMergeabilityInterface.h"
#include <algorithm>
#include <cmath>
#include "paramComputation.h"

// PUBLIC

void PythonMergeabilityInterface::initializeClauses(long long* pyClauses, long long size) {
	// Reset previous values
	m_numVariables = 0;
	m_dirtyLookupTable = true;
	m_clauses.clear();

	// Read and store input
	_convertPyClausesToCpp(pyClauses, size);
}

long long PythonMergeabilityInterface::calculateMergeability(long long* pyVarSet) {
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
	long long totalNumResolvable = 0;
	long long totalNumMergeable = 0;
	ParamComputation::computeMergeability(
		totalNumResolvable, totalNumMergeable, m_clauses, posClauseIndices, negClauseIndices
	);

	return totalNumMergeable;
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
		if (m_posClauseIndices[var - 1].size() != 0 || m_negClauseIndices[var - 1].size() != 0) continue;
		varSet.emplace(var);
	}
}

void PythonMergeabilityInterface::_generateLookupTable() {
	// Allocate memory
	m_posClauseIndices = std::vector<std::vector<unsigned int>>(m_numVariables);
	m_negClauseIndices = std::vector<std::vector<unsigned int>>(m_numVariables);
	m_allClauseIndices = std::vector<std::vector<unsigned int>>(m_numVariables);

	// Generate the lookup tables
	ParamComputation::computeLiteralClauseLookupTable(m_posClauseIndices, m_negClauseIndices, m_clauses);
	ParamComputation::computeVariableClauseLookupTable(m_allClauseIndices, m_posClauseIndices, m_negClauseIndices);

	// Set state flag
	m_dirtyLookupTable = false;
}

void PythonMergeabilityInterface::_getLookupTablesForVarSet (
	std::vector<std::vector<unsigned int>>& posClauseIndices, std::vector<std::vector<unsigned int>>& negClauseIndices,
	const std::set<long long>& varSet
) {
	// Find clauses which contain variables outside of the variable set
	std::set<unsigned int> clausesToFilter;
	for (unsigned int i = 0; i < m_clauses.size(); ++i) {
		for (unsigned int j = 0; j < m_clauses[i].size(); ++j) {
			if (varSet.find(m_clauses[i][j]) == varSet.end()) {
				clausesToFilter.emplace(i);
				break;
			}
		}
	}

	// Copy allowed indices from lookup tables
	for (long long i = 0; i < m_numVariables; ++i) {
		for (unsigned int p_i = 0; p_i < m_posClauseIndices.size(); ++p_i) {
			if (clausesToFilter.find(m_posClauseIndices[i][p_i]) == clausesToFilter.end()) {
				posClauseIndices[i].push_back(m_posClauseIndices[i][p_i]);
			}
		}

		for (unsigned int n_i = 0; n_i < m_negClauseIndices.size(); ++n_i) {
			if (clausesToFilter.find(m_negClauseIndices[i][n_i]) == clausesToFilter.end()) {
				negClauseIndices[i].push_back(m_negClauseIndices[i][n_i]);
			}
		}
	}
}