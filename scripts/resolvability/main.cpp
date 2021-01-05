#include <assert.h>
#include <cmath>
#include <fstream>
#include <functional>
#include <iostream>
#include <set>
#include <string>
#include <vector>
#include "src/mergeabilityCommon.h"
#include "src/paramComputation.h"
#include "src/paramIO.h"

#define OPTION_ALL 'a'
#define OPTION_CVR 'c'
#define OPTION_DEGREE_VECTOR 'd'
#define OPTION_RESOLVABILITY 'r'

// Global options
std::set<char> options;

static void printHelp(const char* command) {
	std::cerr << "Usage: " << command << " <OPTION [OPTIONS...]> <INPUT [INPUTS...]>" << std::endl;
	std::cerr << "\t-" << OPTION_ALL           << ": enable all computations" << std::endl;
	std::cerr << "\t-" << OPTION_CVR           << ": compute CVR" << std::endl;
	std::cerr << "\t-" << OPTION_DEGREE_VECTOR << ": compute degree vector" << std::endl;
	std::cerr << "\t-" << OPTION_RESOLVABILITY << ": compute resolvability, mergeability, mergeability vector, and total clause widths" << std::endl;
}

static int parseInput(std::set<char>& options, std::vector<std::string>& inputFiles, const int argc, const char* const* argv) {
	// Read in option flags and input files
	for (int argIndex = 1; argIndex < argc; ++argIndex) {
		std::string inputStr(argv[argIndex]);
		if (inputStr[0] == '-') { // Value is option
			for (unsigned int i = 1; i < inputStr.size(); ++i) {
				switch (inputStr[i]) {
					case OPTION_ALL:
					case OPTION_CVR:
					case OPTION_DEGREE_VECTOR:
					case OPTION_RESOLVABILITY:
						options.insert(inputStr[i]);
						break;
					default: return 1;
				}
			}
		} else { // Value is input file
			inputFiles.push_back(inputStr);
		}
	}

	// Enable all options if OPTION_ALL is enabled
	if (options.find(OPTION_ALL) != options.end()) {
		options.insert(OPTION_CVR);
		options.insert(OPTION_DEGREE_VECTOR);
		options.insert(OPTION_RESOLVABILITY);
	}

	// Report an error if there are no options
	return options.size() == 0;
}

using namespace std::placeholders;
int main (const int argc, const char* const * argv) {
	// Validate input
	if (argc < 2) {
		printHelp(argv[0]);
		return 1;
	}

	// Parse input
	std::vector<std::string> inputFiles;
	if (parseInput(options, inputFiles, argc, argv)) {
		printHelp(argv[0]);
		return 1;
	}

	for (const std::string& inputFileStr : inputFiles) {
		// Read clauses from file
		static const std::string CNF_EXTENSION = ".cnf";
		// const std::string inputFileBaseStr = inputFileStr.substr(0, inputFileStr.size() - CNF_EXTENSION.size());
		const std::string inputFileBaseStr = inputFileStr;
		long long numVars = 0, numClauses = 0, maxClauseWidth = 0;
		std::vector<std::vector<long long>> clauses;
		if (ParamIO::readClauses(clauses, numVars, numClauses, maxClauseWidth, inputFileStr)) return 1;
		assert(numVars > 0);
		assert(numClauses > 0);
		assert(maxClauseWidth > 0);

		// Calculate and output CVR
		if (options.find(OPTION_CVR) != options.end()) {
			double cvr = 0;
			ParamComputation::computeCVR(cvr, numClauses, numVars);
			assert(cvr > 0);
			ParamIO::writeFile(inputFileBaseStr + ".cvr", std::bind(ParamIO::writeCVR, _1, numClauses, numVars, cvr));
		}

		// Calculate and output degree vector
		if (options.find(OPTION_DEGREE_VECTOR) != options.end()) {
			std::vector<long long> degreeVector(numVars);
			ParamComputation::computeDegreeVector(degreeVector, clauses);
			ParamIO::writeFile(inputFileBaseStr + ".dv", std::bind(ParamIO::writeDegreeVector, _1, degreeVector));
		}

		// Calculate and output num resolvable and num mergeable
		if (options.find(OPTION_RESOLVABILITY) != options.end()) {
			ParamComputation::ResolvabilityMergeabilityOutput resolvabilityMergeabilityOutput{};
			resolvabilityMergeabilityOutput.mergeabilityVector = std::vector<long long>(maxClauseWidth + 1);
			resolvabilityMergeabilityOutput.mergeabilityScoreVector = std::vector<long long>(MSV_NUM_BUCKETS + 1);
			ParamComputation::computeResolvable(&resolvabilityMergeabilityOutput, clauses, numVars);
			assert(resolvabilityMergeabilityOutput.totalNumResolvable >= 0);
			assert(resolvabilityMergeabilityOutput.totalNumResolvable >= 0);

			ParamIO::writeFile(inputFileBaseStr + ".tcw", std::bind(ParamIO::writeClauseWidths, _1,
				resolvabilityMergeabilityOutput.preResolutionClauseWidth,
				resolvabilityMergeabilityOutput.postResolutionClauseWidth
			));
			ParamIO::writeFile(inputFileBaseStr + ".rvm", std::bind(ParamIO::writeResolvability, _1,
				resolvabilityMergeabilityOutput.totalNumResolvable,
				resolvabilityMergeabilityOutput.totalNumMergeable,
				resolvabilityMergeabilityOutput.mergeabilityScore1,
				resolvabilityMergeabilityOutput.mergeabilityScore2
			));
			ParamIO::writeFile(inputFileBaseStr + ".mv", std::bind(ParamIO::writeMergeabilityVector, _1,
				resolvabilityMergeabilityOutput.mergeabilityVector
			));
			ParamIO::writeFile(inputFileBaseStr + ".msv", std::bind(ParamIO::writeMergeabilityScoreVector, _1,
				resolvabilityMergeabilityOutput.mergeabilityScoreVector
			));
		}
	}

	return 0;
}
