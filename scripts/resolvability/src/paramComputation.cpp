#include "paramComputation.h"
#include "mergeabilityCommon.h"
#include <algorithm>
#include <cmath>
#include <set>

// PUBLIC

void ParamComputation::computeCVR(double& cvr, long long numClauses, long long numVars) {
	cvr = numClauses / static_cast<double>(numVars);
}

void ParamComputation::computeResolvable(
	ResolvabilityMergeabilityOutput* resolvabilityMergeabilityOutput,
	const std::vector<std::vector<long long>>& clauses, long long numVariables
) {
	// Generate the lookup tables
	std::vector<std::vector<unsigned int>> posClauseIndices(numVariables);
	std::vector<std::vector<unsigned int>> negClauseIndices(numVariables);
	ParamComputation::computeLiteralClauseLookupTable(posClauseIndices, negClauseIndices, clauses);

	// Compute parameters using lookup tables
	computeResolvable(resolvabilityMergeabilityOutput, clauses, posClauseIndices, negClauseIndices);
}

void ParamComputation::computeMergeability(
	long long& totalNumResolvable, long long& totalNumMergeable,
	const std::vector<std::vector<long long>>& clauses, long long numVariables
) {
	// Generate the lookup tables
	std::vector<std::vector<unsigned int>> posClauseIndices(numVariables);
	std::vector<std::vector<unsigned int>> negClauseIndices(numVariables);
	ParamComputation::computeLiteralClauseLookupTable(posClauseIndices, negClauseIndices, clauses);

	// Compute parameters using lookup tables
	computeMergeability(totalNumResolvable, totalNumMergeable, clauses, posClauseIndices, negClauseIndices);
}

void ParamComputation::computeDegreeVector(std::vector<long long>& degreeVector, std::vector<std::vector<long long>>& clauses) {
	// Iterate through every variable of every clause
	for (const std::vector<long long>& clause : clauses) {
		for (long long x : clause) {
			// Increment corresponding variable in degree vector
			++degreeVector[std::abs(x) - 1];
		}
	}

	std::sort(degreeVector.rbegin(), degreeVector.rend());
}

// PRIVATE

void ParamComputation::computeLiteralClauseLookupTable(
	std::vector<std::vector<unsigned int>>& posClauseIndices, std::vector<std::vector<unsigned int>>& negClauseIndices,
	const std::vector<std::vector<long long>>& clauses
) {
	for (unsigned int i = 0; i < clauses.size(); ++i) {
		for (unsigned int c_i = 0; c_i < clauses[i].size(); ++c_i) {
			const int var = clauses[i][c_i];
			if (var > 0) { // The variable should never be zero
				posClauseIndices[+var - 1].emplace_back(i);	
			} else {
				negClauseIndices[-var - 1].emplace_back(i);
			}
		}
	}
}

void ParamComputation::computeVariableClauseLookupTable(
	std::vector<std::vector<unsigned int>>& allClauseIndices,
	std::vector<std::vector<unsigned int>>& posClauseIndices,
	std::vector<std::vector<unsigned int>>& negClauseIndices
) {
	// Sort literal-clause lookup tables and generate sorted variable-clause lookup table
	// O(n deg(v) log(deg(v)))
	for (unsigned int i = 0; i < allClauseIndices.size(); ++i) {
		// Sort the literal-clause lookup table for each variable
		// O(deg(v) log(deg(v)))
		std::sort(posClauseIndices[i].begin(), posClauseIndices[i].end());
		std::sort(negClauseIndices[i].begin(), negClauseIndices[i].end());
		
		// Generate variable-clause lookup table by merging lookup tables
		// O(deg(v))
		unsigned int p_i = 0, n_i = 0;
		while (p_i < posClauseIndices[i].size() && n_i < negClauseIndices[i].size()) {
			if (p_i < n_i) {
				allClauseIndices[i].push_back(posClauseIndices[i][p_i]);
				++p_i;
			} else if (p_i > n_i) {
				allClauseIndices[i].push_back(negClauseIndices[i][n_i]);
				++n_i;
			} else {
				allClauseIndices[i].push_back(posClauseIndices[i][p_i]);
				++p_i;
				++n_i;
			}
		}

		// Finish merging lookup table for positive literals
		while (p_i < posClauseIndices[i].size()) {
			allClauseIndices[i].push_back(posClauseIndices[i][p_i]);
			++p_i;
		}

		// Finish merging lookup table for negative literals
		while (p_i < posClauseIndices[i].size()) {
			allClauseIndices[i].push_back(negClauseIndices[i][n_i]);
			++n_i;
		}
	}
}

void ParamComputation::forEachResolvable(
	const std::vector<std::vector<unsigned int>>& posClauseIndices,
	const std::vector<std::vector<unsigned int>>& negClauseIndices,
	const std::vector<std::vector<long long>>& clauses, ResolvabilityCallback callback
) {
	// Find all clauses which resolve on a variable
	// O((max_degree(v))^2 k^2 log(k))
	const long long numVariables = posClauseIndices.size();
	for (long long i = 0; i < numVariables; ++i) {
		const std::vector<unsigned int>& posClauses = posClauseIndices[i];
		const std::vector<unsigned int>& negClauses = negClauseIndices[i];
		
		// Check for clauses which resolve on the variable
		// O((max_degree(v))^2 k log(k))
		for (unsigned int c_i : posClauses) {
			const std::vector<long long>& posClause = clauses[c_i];

			// Initialize set for checking resolvability
			// O(k log(k))
			std::set<long long> found;
			for (long long var : posClause) {
				found.insert(var);
			}

			// Check if any of the negative clause resolves with the positive clause
			// O((max_degree(v)) k log(k))
			for (unsigned int c_j : negClauses) {
				const std::vector<long long>& negClause = clauses[c_j];

				// Check for resolvable/mergeable clauses
				// O(k log(k))
				bool resolvable = false; // True if there is exactly one opposing literal
				long long tmpNumMergeable = 0;
				for (unsigned int k = 0; k < negClause.size(); ++k) {
					if (found.find(-negClause[k]) != found.end()) {
						if (resolvable) {
							resolvable = false;
							break;
						}
						resolvable = true;
					} else if (found.find(negClause[k]) != found.end()) {
						++tmpNumMergeable;
					}
				}

				// Execute callback if resolvable 
				if (resolvable) callback(tmpNumMergeable, posClause, negClause);
			}
		}
	}
}

// O((max_degree(v))^2 k^2 log(k) + (m k)) 
void ParamComputation::computeResolvable(
	ResolvabilityMergeabilityOutput* resolvabilityMergeabilityOutput,
	const std::vector<std::vector<long long>>& clauses,
	const std::vector<std::vector<unsigned int>>& posClauseIndices,
	const std::vector<std::vector<unsigned int>>& negClauseIndices
) {
	// Get total clause width
	for (unsigned int i = 0; i < clauses.size(); ++i) {
		resolvabilityMergeabilityOutput->preResolutionClauseWidth += static_cast<long long>(clauses[i].size());
	}

	ResolvabilityCallback callback = [&](
		long long tmpNumMergeable,
		const std::vector<long long>& posClause,
		const std::vector<long long>& negClause
	) {
		++(resolvabilityMergeabilityOutput->totalNumResolvable);
		++(resolvabilityMergeabilityOutput->mergeabilityVector[tmpNumMergeable]);
		resolvabilityMergeabilityOutput->totalNumMergeable += tmpNumMergeable;

		// Calculate normalized mergeability score
		const int totalClauseSize = static_cast<int>(posClause.size() + negClause.size());
		if (totalClauseSize > 2) {
			const double tmpMergeabilityScore  = tmpNumMergeable / static_cast<double>(totalClauseSize - 2);
			const double tmpMergeabilityScore2 = tmpNumMergeable / static_cast<double>(totalClauseSize - tmpNumMergeable - 2);
			resolvabilityMergeabilityOutput->mergeabilityScore1 += tmpMergeabilityScore;
			resolvabilityMergeabilityOutput->mergeabilityScore2 += tmpMergeabilityScore2;

			// Add to histogram
			// index = [ (local mergeability score) / (max mergeability score) ] * (num buckets)
			const int scoreVectorIndex = static_cast<int>(std::floor(MAX_MERGEABILITY_SCORE_INV * MSV_NUM_BUCKETS * tmpMergeabilityScore));
			++(resolvabilityMergeabilityOutput->mergeabilityScoreVector[scoreVectorIndex]);
		}

		// Add to total post-resolution clause size
		const long long postResolutionClauseSize = static_cast<long long>(totalClauseSize - tmpNumMergeable - 2);
		resolvabilityMergeabilityOutput->postResolutionClauseWidth += static_cast<long long>(postResolutionClauseSize);
	};

	forEachResolvable(posClauseIndices, negClauseIndices, clauses, callback);
}

void ParamComputation::computeMergeability(
	long long& totalNumResolvable, long long& totalNumMergeable,
	const std::vector<std::vector<long long>>& clauses,
	const std::vector<std::vector<unsigned int>>& posClauseIndices,
	const std::vector<std::vector<unsigned int>>& negClauseIndices
) {
	ResolvabilityCallback callback = [&](
		long long localNumMergeable,
		const std::vector<long long>& /* posClause */,
		const std::vector<long long>& /* negClause */
	) {
		++totalNumResolvable;
		totalNumMergeable += localNumMergeable;
	};

	forEachResolvable(posClauseIndices, negClauseIndices, clauses, callback);
}