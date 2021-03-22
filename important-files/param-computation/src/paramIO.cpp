#include "paramIO.h"
#include "mergeabilityCommon.h"
#include <fstream>
#include <iostream>
#include <sstream>

int ParamIO::readClauses(std::vector<std::vector<long long>>& clauses, long long& numVars, long long& numClauses, long long& maxClauseWidth, const std::string& inputFileStr) {
	std::ifstream file(inputFileStr);
	if (!file.is_open()) {
		std::cerr << "Error while opening: " << inputFileStr << std::endl;
		return 1;
	}

	// Read CNF header
	bool gotHeader = false;
	std::string lineStr;
	while (!gotHeader) {
		std::getline(file, lineStr);
		if (file.bad()) return 1;
		if (lineStr.size() == 0) continue; // Skip empty lines

		std::stringstream line(lineStr);
		char firstChar = 0;
		line >> firstChar; if (line.bad()) return 1;
		if (firstChar == 'c') continue;	// Skip comments
		if (firstChar != 'p') {
			std::cerr << "Invalid header line" << std::endl;
			return 1;
		}

		std::string cnfString;
		line >> cnfString; if (line.bad()) return 1;
		if (cnfString != "cnf") {
			std::cerr << "Invalid header line" << std::endl;
		}
		line >> numVars >> numClauses; if (line.bad()) return 1;
		gotHeader = true;
	}

	// Reserve memory
	clauses.reserve(numClauses);

	// Read clauses
	std::vector<long long> clause;
	while (std::getline(file, lineStr)) {
		if (lineStr.size() == 0) continue; // Skip empty lines
	
		std::stringstream line(lineStr);
		long long var = 0;
		while (line.good()) {
			line >> var; if (line.bad()) return 1;
			if (var == 0) { // Clauses end upon reading zero
				clauses.push_back(clause);
				maxClauseWidth = std::max(maxClauseWidth, static_cast<long long>(clause.size()));
				clause.clear();
			} else {
				clause.push_back(var);
			}
		}
	}
	return 0;
}

int ParamIO::writeFile(const std::string& outputFileStr, std::function<void(std::ofstream&)> writerFunc) {
	std::ofstream outputFile(outputFileStr);
	if (!outputFile.is_open()) {
		std::cerr << "Error while opening: " << outputFileStr << std::endl;
		return 1;
	}

	writerFunc(outputFile);
	if (outputFile.bad()) {
		std::cerr << "Error while writing: " << outputFileStr << std::endl;
		return 1;
	}

	return 0;
}

void ParamIO::writeCVR(std::ofstream& outFile, long long numClauses, long long numVars, double cvr) {
	outFile <<
		numClauses << " " <<
		numVars    << " " <<
		cvr        << std::endl;
}

void ParamIO::writeResolvability(std::ofstream& outFile, long long numResolvable, long long numMergeable, double mergeabilityScore1, double mergeabilityScore2) {
	outFile <<
		numResolvable      << " " <<
		numMergeable       << " " <<
		mergeabilityScore1 << " " <<
		mergeabilityScore2 << std::endl;
}

void ParamIO::writeDegreeVector(std::ofstream& outFile, std::vector<long long>& degreeVector) {
	for (unsigned int i = 0; i < degreeVector.size(); ++i) {
		outFile << i + 1 << " " << degreeVector[i] << std::endl;
	}
}

void ParamIO::writeMergeabilityScoreVector(std::ofstream& outFile, std::vector<long long>& mergeabilityScoreVector) {
	for (int i = 0; i <= MSV_NUM_BUCKETS; ++i) {
		outFile << (i * MAX_MERGEABILITY_SCORE) / static_cast<double>(MSV_NUM_BUCKETS) << " " << mergeabilityScoreVector[i] << std::endl;
	}
}

void ParamIO::writeClauseWidths(std::ofstream& outFile, long long totalOriginalClauseWidth, long long totalPostResClauseWidth) {
	outFile << totalOriginalClauseWidth << " " << totalPostResClauseWidth << std::endl;
}