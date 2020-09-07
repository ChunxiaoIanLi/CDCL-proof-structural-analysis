#ifndef PY_MERGEABILITY_H
#define PY_MERGEABILITY_H

#include <set>
#include <vector>

class PythonMergeabilityInterface {
public:
	/**
	 * @brief Store python clauses in C++
	 * @param pyClauses 1D array storing clauses separated by zeros
	 * @param size The total length of the array
	 */
	void initializeClauses(long long* pyClauses, long long size);

	/**
	 * @brief Calculate the total number of mergeable literal pairs over the subset of clauses containing only variables in the
	 * variable set
	 * @param varSet The variables by which clauses should be filtered when computing mergeability
	 */
	long long calculateMergeability(long long* varSet);

private:
	void _convertPyClausesToCpp(long long* pyClauses, long long size);
	void _convertPyVarSetToCpp(std::set<long long>& varSet, long long* pyVarSet);
	void _generateLookupTable();
	void _getLookupTablesForVarSet(
		std::vector<std::vector<unsigned int>>& posClauseIndices, std::vector<std::vector<unsigned int>>& negClauseIndices,
		const std::set<long long>& varSet
	);

	bool m_dirtyLookupTable = false;
	long long m_numVariables = 0;
	std::vector<std::vector<long long>> m_clauses;
	std::vector<std::vector<unsigned int>> m_posClauseIndices;
	std::vector<std::vector<unsigned int>> m_negClauseIndices;
	std::vector<std::vector<unsigned int>> m_allClauseIndices;
};

#endif // PY_MERGEABILITY_H