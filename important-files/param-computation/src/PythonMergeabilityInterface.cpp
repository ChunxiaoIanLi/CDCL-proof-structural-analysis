#include "PythonMergeabilityInterface.h"
#include <algorithm>
#include <cmath>
#include <iostream>
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

void PythonMergeabilityInterface::calculateMergeabilityScore(long long* pyVarSet, int clauseFilterMode) {
	// Generate variable->clause lookup table
	if (m_dirtyLookupTable) _generateLookupTable();

	// Reset output values
	ParamComputation::resetOutput(m_output);
	m_output.mergeabilityScoreVector = std::vector<long long>(MSV_NUM_BUCKETS + 1);
	m_numClauses = 0;
	m_output.preResolutionClauseWidth = 0;

	// Read variable set
	std::set<long long> varSet;
	_convertPyVarSetToCpp(varSet, pyVarSet);

	// Filter clauses by variable set
	std::vector<std::vector<unsigned int>> posClauseIndices(m_numVariables);
	std::vector<std::vector<unsigned int>> negClauseIndices(m_numVariables);

	std::vector<std::vector<long long>> clausesCopy;
	std::vector<std::vector<long long>>* clauses = NULL;
	switch (clauseFilterMode) {
		case 0: {
			_getLookupTablesForVarSet(posClauseIndices, negClauseIndices, varSet);
			clauses = &m_clauses;
		} break;
		case 1:
		default: {
			_copyClausesForVarSet(clausesCopy, varSet);
			ParamComputation::computeLiteralClauseLookupTable(posClauseIndices, negClauseIndices, clausesCopy);
			clauses = &clausesCopy;
		} break;
	}


	// Save the pre-resolution clause width because this gets overwritten by computeResolvable
	const long long preResolutionClauseWidth = m_output.preResolutionClauseWidth;
	m_output.preResolutionClauseWidth = 0;

	// Calculate mergeability over the acceptable clauses
	ParamComputation::computeResolvable(&m_output, *clauses, posClauseIndices, negClauseIndices);

	// Load back the correct value of pre-resolution clause width
	m_output.preResolutionClauseWidth = preResolutionClauseWidth;
}

double PythonMergeabilityInterface::getCVR() {
	return m_output.cvr;
}

long PythonMergeabilityInterface::getMergeability() {
	return m_output.totalNumMergeable;
}

long PythonMergeabilityInterface::getResolvability() {
	return m_output.totalNumResolvable;
}

double PythonMergeabilityInterface::getMergeabilityScore1Norm1() {
	return m_output.mergeabilityScore1 / static_cast<double>(m_output.totalNumResolvable);
}

double PythonMergeabilityInterface::getMergeabilityScore1Norm2() {
	const double m = static_cast<double>(m_numClauses);
	return m_output.mergeabilityScore1 / (m * m);
}

double PythonMergeabilityInterface::getMergeabilityScore2Norm1() {
	return m_output.mergeabilityScore2 / static_cast<double>(m_output.totalNumResolvable);
}

double PythonMergeabilityInterface::getMergeabilityScore2Norm2() {
	const double m = static_cast<double>(m_numClauses);
	return m_output.mergeabilityScore2 / (m * m);
}

double PythonMergeabilityInterface::getPreResolutionClauseWidth() {
	// Return 0 if there are no clauses in the variable set
	if (m_numClauses == 0) return 0;

	return m_output.preResolutionClauseWidth / static_cast<double>(m_numClauses);
}

double PythonMergeabilityInterface::getPostResolutionClauseWidth() {
	// Return 0 if there are no resolvable clauses
	if (m_output.totalNumResolvable == 0) return 0;

	return m_output.postResolutionClauseWidth / static_cast<double>(m_output.totalNumResolvable);
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
	// Initialize data structures for computing CVR over the clause subset
	m_numClauses = 0;
	std::set<long long> vars;

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
			++m_numClauses;
			m_output.preResolutionClauseWidth += m_clauses[i].size();
			for (unsigned int j = 0; j < m_clauses[i].size(); ++j) {
				const int var = m_clauses[i][j];
				if (var > 0) { // The variable should never be zero
					posClauseIndices[+var - 1].emplace_back(i);
					vars.insert(var);
				} else {
					negClauseIndices[-var - 1].emplace_back(i);
					vars.insert(-var);
				}
			}
		}
	}

	// Calculate CVR over the clause subset
	m_output.cvr = m_numClauses / static_cast<double>(vars.size());
}

void PythonMergeabilityInterface::_copyClausesForVarSet(
	std::vector<std::vector<long long>>& clausesCopy,
	const std::set<long long>& varSet
) {
	// Initialize data structures for computing CVR over the clause subset
	std::set<long long> vars;

	for (unsigned int i = 0; i < m_clauses.size(); ++i) {
		// Copy the subset of the clause which appears in the variable set
		std::vector<long long> clauseCopy;
		for (unsigned int j = 0; j < m_clauses[i].size(); ++j) {
			if (varSet.find(std::abs(m_clauses[i][j])) != varSet.end()) {
				clauseCopy.emplace_back(m_clauses[i][j]);
			}
		}

		// Add the clause only if at least one of the requested variables was found
		if (clauseCopy.size() > 0) {
			clausesCopy.emplace_back(clauseCopy);
			m_output.preResolutionClauseWidth += clauseCopy.size();

			for (long long literal : clauseCopy) vars.insert(std::abs(literal));
		}
	}

	m_numClauses = clausesCopy.size();
	m_output.cvr = m_numClauses / static_cast<double>(vars.size());
}
