#ifndef PARAM_IO_H
#define PARAM_IO_H

#include <functional>
#include <string>
#include <vector>

class ParamIO {
public:
	/**
	 * @brief Read clauses from file
	 * @param clauses The 2D array into which to write the clauses
	 * @param numVars The address into which to write the number of variables
	 * @param numClauses The address into which to write the number of clauses
	 * @param maxClauseWidth The address into which to write maximum width of a clause
	 * @param inputFileStr The name of the file to read
	 * @return 0 on success, 1 otherwise
	 */
	static int readClauses(
		std::vector<std::vector<long long>>& clauses, long long& numVars, long long& numClauses, long long& maxClauseWidth,
		const std::string& inputFileStr
	);

	/**
	 * @brief A wrapper function for writing to file and handling IO errors. Parameters to the writer function should be bound.
	 * @param outputFileStr The name of the file to write to
	 * @param writerFunc The function which is given a file stream object and does the actual writing
	 * @return 0 on success, 1 otherwise
	 */
	static int writeFile(const std::string& outputFileStr, std::function<void(std::ofstream&)> writerFunc);
	
	/**
	 * @brief Write the number of clauses, number of variables, and clause-variable ratio to file (space-separated)
	 * @param outFile The file stream to write to
	 * @param numClauses The number of clauses
	 * @param numVars The number of variables
	 * @param cvr The clause-variable ratio
	 */
	static void writeCVR(std::ofstream& outFile, long long numClauses, long long numVars, double cvr);

	/**
	 * @brief Write the total number of resolvable clause pairs, the total number of mergeable literal pairs, and the two
	 * normalized mergeability scores to file (space-separated)
	 * @param outFile The file stream to write to
	 * @param numResolvable The total number of resolvable clause pairs
	 * @param numMergeable The total number of mergeable literal pairs
	 * @param mergeabilityScore1 The sum over all mergeable literal pairs of ((numMergeable) / (width(resolvingClause1) +
	 * width(resolvingClause2) - 2))
	 * @param mergeabilityScore2 The sum over all mergeable literal pairs of ((numMergeable) / (width(resolvingClause1) +
	 * width(resolvingClause2) - numMergeable - 2))
	 */
	static void writeResolvability(
		std::ofstream& outFile, long long numResolvable, long long numMergeable, double mergeabilityScore1,
		double mergeabilityScore2
	);

	/**
	 * @brief Write the degree vector to file, with the index and degree space-separated on each line
	 * @param outFile The file stream to write to
	 * @param degreeVector The sorted degree vector to write
	 */
	static void writeDegreeVector(std::ofstream& outFile, std::vector<long long>& degreeVector);

	/**
	 * @brief Write the mergeability score vector to file, with the index and degree space-separated on each line. This
	 * uses the first definition of the normalized mergeability score (maximum score of 0.5)
	 * @param outFile The file stream to write to
	 * @param mergeabilityScoreVector The mergeability score vector to write
	 */
	static void writeMergeabilityScoreVector(std::ofstream& outFile, std::vector<long long>& mergeabilityScoreVector);

	/**
	 * @brief Write the sum of the pre-resolution clause widths and the sum of the post-resolution clause widths to file
	 * (space-separated)
	 * @param outFile The file stream to write to
	 * @param totalOriginalClauseWidth The sum of all pre-resolution clause widths
	 * @param totalPostResClauseWidth The sum of post-resolution clause widths over resolving clauses
	 */
	static void writeClauseWidths(
		std::ofstream& outFile, long long totalOriginalClauseWidth, long long totalPostResClauseWidth
	);
};

#endif // PARAM_IO_H