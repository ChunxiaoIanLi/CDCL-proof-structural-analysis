#include <algorithm>
#include <fstream>
#include <functional>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>

#define MAX_LINE_SIZE 2048
#define RESOLVABLE_SHIFT 0
#define MERGEABLE_SHIFT 1
#define RESOLVABLE_MASK (0x1 << RESOLVABLE_SHIFT)
#define MERGEABLE_MASK (0x1 << MERGEABLE_SHIFT)

// Read clauses from file
static int readClauses(std::vector<std::vector<int>>& clauses, int& numVars, int& numClauses, std::ifstream& file) {
	char buffer[MAX_LINE_SIZE];

	// Read CNF header
	bool gotHeader = false;
	while (!gotHeader) {
		file.getline(buffer, MAX_LINE_SIZE);
		if (file.bad()) return 1;
		if (buffer[0] == 0) continue; // Skip empty lines

		std::stringstream line(buffer);
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
	std::vector<int> clause;
	while (file.good()) {
		file.getline(buffer, MAX_LINE_SIZE);
		if (file.bad()) return 1;
		if (buffer[0] == 0) continue; // Skip empty lines
	
		std::stringstream line(buffer);
		int var = 0;
		while (line.good()) {
			line >> var; if (line.bad()) return 1;
			if (var == 0) { // Clauses end upon reading zero
				clauses.push_back(clause);
				clause.clear();
			} else {
				clause.push_back(var);
			}
		}
	}
	return 0;
}

static int countResolvable(int& numResolvable, int& numMergeable, const std::vector<std::vector<int>>& clauses) {
	for (unsigned int i = 0; i < clauses.size(); ++i) {
		// Initialize set for checking resolvability
		std::set<int> found;
		for (unsigned int c_i = 0; c_i < clauses[i].size(); ++c_i) {
			found.insert(clauses[i][c_i]);
		}

		// Compare every clause with every other clause
		for (unsigned int j = i + 1; j < clauses.size(); ++j) {
			bool resolvable = false;
			long tmpNumMergeable = 0;
			
			// Check for resolvable/mergeable clauses
			for (unsigned int c_j = 0; c_j < clauses[j].size(); ++c_j) {
				if (found.find(-clauses[j][c_j]) != found.end()) {
					if (resolvable) {
						resolvable = false;
						break;
					}
					resolvable = true;
				} else if (found.find(clauses[j][c_j]) != found.end()) {
					++tmpNumMergeable;
				}
			}

			// Update counts
			if (resolvable) {
				numResolvable += 1;
				numMergeable  += tmpNumMergeable;
			}
		}
	}

	return 0;
}

static int computeDegreeVector(std::vector<int>& degreeVector, std::vector<std::vector<int>>& clauses) {
	// Iterate through every variable of every clause
	for (const std::vector<int>& clause : clauses) {
		for (int x : clause) {
			// Increment corresponding variable in degree vector
			++degreeVector[std::abs(x) - 1];
		}
	}

	std::sort(degreeVector.rbegin(), degreeVector.rend());

	return 0;
}

static int writeFile(const std::string& outputFileStr, std::function<int(std::ofstream&)> writerFunc) {
	std::ofstream outputFile(outputFileStr);
	if (!outputFile.is_open()) {
		std::cerr << "Error while opening: " << outputFileStr << std::endl;
		return 1;
	}

	return writerFunc(outputFile);
}

static int writeCVR(std::ofstream& outFile, double cvr) {
	outFile << cvr << std::endl;
	return 0;
}

static int writeResolvability(std::ofstream& outFile, int numResolvable, int numMergeable) {
	outFile << numResolvable << "," << numMergeable << std::endl;
	return 0;
}

static int writeDegreeVector(std::ofstream& outFile, std::vector<int>& degreeVector) {
	for (unsigned int i = 0; i < degreeVector.size(); ++i) {
		outFile << i + 1 << "," << degreeVector[i] << std::endl;
	}
	return 0;
}

using namespace std::placeholders;
int main (const int argc, const char* const * argv) {
	if (argc < 2) {
		std::cerr << "Usage: " << argv[0] << " <INPUT [INPUTS...]>" << std::endl;
		return 1;
	}

	int argIndex = 1;

	while (argIndex != argc) {
		// Open file
		const std::string inputFileStr(argv[argIndex]);
		std::ifstream inputFile(inputFileStr);
		if (!inputFile.is_open()) {
			std::cerr << "Error while opening: " << inputFileStr << std::endl;
			return 1;
		}

		// Read clauses from file
		int numVars = 0, numClauses = 0;
		std::vector<std::vector<int>> clauses;
		if (readClauses(clauses, numVars, numClauses, inputFile)) {
			std::cerr << "Error while reading: " << inputFileStr << std::endl;
			return 1;
		}

		// Calculate CVR
		double cvr = numClauses / static_cast<double>(numVars);

		// Calculate num resolvable and num mergeable
		int numResolvable = 0, numMergeable = 0;
		if (countResolvable(numResolvable, numMergeable, clauses)) {
			std::cerr << "Error while counting num resolvable for: " << inputFileStr << std::endl;
			return 1;
		}

		// Calculate degree vector
		std::vector<int> degreeVector(numVars);
		if (computeDegreeVector(degreeVector, clauses)) {
			std::cerr << "Error while computing degree vector" << std::endl;
			return 1;
		}

		// Write results to file
		writeFile(inputFileStr + ".cvr", std::bind(writeCVR,           _1, cvr));
		writeFile(inputFileStr + ".rvm", std::bind(writeResolvability, _1, numResolvable, numMergeable));
		writeFile(inputFileStr + ".dv",  std::bind(writeDegreeVector,  _1, degreeVector));

		++argIndex;
	}

	return 0;
}
