#ifndef PARAM_COMPUTATION_H
#define PARAM_COMPUTATION_H

#include <vector>

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
		long long preResolutionClauseWidth = 0; // The sum of the widths of all the clauses before resolution
		long long postResolutionClauseWidth = 0; // The sum of the widths of all the resolved clauses after resolution
		long long totalNumResolvable = 0; // The total number of resolvable clause pairs
		long long totalNumMergeable = 0; // The total number of mergeable literal pairs
		double mergeabilityScore1 = 0; // The sum of ((numMergeable) / (width(resolvingClause1) + width(resolvingClause2) - 2)) over all mergeable literal pairs
		double mergeabilityScore2 = 0; // The sum of ((numMergeable) / (width(resolvingClause1) + width(resolvingClause2) - numMergeable - 2)) over all mergeable literal pairs
		std::vector<long long> mergeabilityVector{}; // A vector for counting the number of occurences of a given number of mergeable literal pairs
		std::vector<long long> mergeabilityScoreVector{}; // A vector for counting the number of occurences of a given mergeability score 
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
};

#endif // PARAM_COMPUTATION_H