#ifndef PARAM_COMPUTATION_H
#define PARAM_COMPUTATION_H

#include <functional>
#include <vector>

// Forward Declarations
class PythonMergeabilityInterface;

class ParamComputation {
public:
	/**
	 * @brief Compute the clause-variable ratio
	 * @param cvr The address into which to write the clause-variable ratio
	 * @param numClauses The number of clauses in the instance
	 * @param numVars The number of variables in the instance
	 */
	static void computeCVR(double& cvr, long long numClauses, long long numVars);

	/** A wrapper object for holding the output of the computeResolvable function */
	struct ResolvabilityMergeabilityOutput {
		// The sum of the widths of all the clauses before resolution
		long long preResolutionClauseWidth = 0;
		// The sum of the widths of all the resolved clauses after resolution
		long long postResolutionClauseWidth = 0;
		// The total number of resolvable clause pairs
		long long totalNumResolvable = 0;
		// The total number of mergeable literal pairs
		long long totalNumMergeable = 0;
		// The sum of ((numMergeable) / (width(resolvingClause1) + width(resolvingClause2) - 2)) over all mergeable literal
		// pairs
		double mergeabilityScore1 = 0;
		// The sum of ((numMergeable) / (width(resolvingClause1) + width(resolvingClause2) - numMergeable - 2)) over all
		// mergeable literal pairs
		double mergeabilityScore2 = 0;
		// A vector for counting the number of occurences of a given number of mergeable literal pairs
		std::vector<long long> mergeabilityVector{};
		// A vector for counting the number of occurences of a given mergeability score 
		std::vector<long long> mergeabilityScoreVector{};
	};

	/**
	 * @brief Compute parameters related to resolvability and mergeability
	 * @param resolvabilityMergeabilityOutput The address into which to write the computed resolvability and mergeability values
	 * @param clauses The clauses over which to compute resolvability and mergeability
	 * @param numVariables The number of distinct variables in clauses
	 */
	static void computeResolvable(
		ResolvabilityMergeabilityOutput* resolvabilityMergeabilityOutput,
		const std::vector<std::vector<long long>>& clauses, long long numVariables
	);

	/**
	 * @brief Compute parameters related to resolvability and mergeability
	 * @param totalNumResolvable The address into which to write the total number of resolvable clause pairs
	 * @param totalNumMergeable The address into which to write the total number of mergeable literal pairs
	 * @param clauses The clauses over which to compute resolvability and mergeability
	 * @param numVariables The number of distinct variables in clauses
	 */
	static void computeMergeability(
		long long& totalNumResolvable, long long& totalNumMergeable,
		const std::vector<std::vector<long long>>& clauses, long long numVariables
	);

	/**
	 * @brief Compute the degree vector
	 * @param degreeVector A vector to hold the degree vector output
	 * @param clauses The clauses over which to compute the degree vector
	 */
	static void computeDegreeVector(std::vector<long long>& degreeVector, std::vector<std::vector<long long>>& clauses);

private:
	/**
	 * @brief Compute the literal-clause lookup table
	 * @param posClauseIndices Address to write clause indices for positive literals, with preallocated space for all variables
	 * @param negClauseIndices Address to write clause indices for negative literals, with preallocated space for all variables
	 * @param clauses The clauses over which to compute the lookup table
	 */
	static void computeLiteralClauseLookupTable(
		std::vector<std::vector<unsigned int>>& posClauseIndices, std::vector<std::vector<unsigned int>>& negClauseIndices,
		const std::vector<std::vector<long long>>& clauses
	);

	/**
	 * @brief Compute the variable-clause lookup table
	 * @param allClauseIndices Address to write clause indices, with preallocated space for all variables
	 * @param posClauseIndices Clause indices for positive literals
	 * @param negClauseIndices Clause indices for negative literals
	 */
	static void computeVariableClauseLookupTable(
		std::vector<std::vector<unsigned int>>& allClauseIndices,
		std::vector<std::vector<unsigned int>>& posClauseIndices,
		std::vector<std::vector<unsigned int>>& negClauseIndices
	);

	/**
	 * @brief Callback function for resolvability computation
	 * @param 1 the local number of mergeable literal pairs
	 * @param 2 the clause with the positive resolving literal
	 * @param 2 the clause with the negative resolving literal
	 */
	using ResolvabilityCallback = std::function<void(long long, const std::vector<long long>&, const std::vector<long long>&)>;

	/**
	 * @brief Compute resolvable clause pairs and call the callback function for every resolvable clause pair
	 * @param posClauseIndices literal-clause lookup table for positive literals
	 * @param negClauseIndices literal-clause lookup table for negative literals
	 * @param clauses The clauses over which to compute resolvability
	 * @param callback The function to call for each resolvable clause pair
	 */
	static void forEachResolvable(
		const std::vector<std::vector<unsigned int>>& posClauseIndices,
		const std::vector<std::vector<unsigned int>>& negClauseIndices,
		const std::vector<std::vector<long long>>& clauses, ResolvabilityCallback callback
	);

	/**
	 * @brief Compute parameters related to resolvability and mergeability
	 * @param resolvabilityMergeabilityOutput The address into which to write the computed resolvability and mergeability values
	 * @param clauses The clauses over which to compute resolvability and mergeability
	 * @param posClauseIndices literal-clause lookup table for positive literals
	 * @param negClauseIndices literal-clause lookup table for negative literals
	 */
	static void computeResolvable(
		ResolvabilityMergeabilityOutput* resolvabilityMergeabilityOutput,
		const std::vector<std::vector<long long>>& clauses,
		const std::vector<std::vector<unsigned int>>& posClauseIndices,
		const std::vector<std::vector<unsigned int>>& negClauseIndices
	);

	/**
	 * @brief Compute parameters related to resolvability and mergeability
	 * @param totalNumResolvable The address into which to write the total number of resolvable clause pairs
	 * @param totalNumMergeable The address into which to write the total number of mergeable literal pairs
	 * @param clauses The clauses over which to compute resolvability and mergeability
	 * @param posClauseIndices literal-clause lookup table for positive literals
	 * @param negClauseIndices literal-clause lookup table for negative literals
	 */
	static void computeMergeability(
		long long& totalNumResolvable, long long& totalNumMergeable,
		const std::vector<std::vector<long long>>& clauses,
		const std::vector<std::vector<unsigned int>>& posClauseIndices,
		const std::vector<std::vector<unsigned int>>& negClauseIndices
	);

	// PythonMergeabilityInterface needs special access to helper functions
	friend class PythonMergeabilityInterface;
};

#endif // PARAM_COMPUTATION_H