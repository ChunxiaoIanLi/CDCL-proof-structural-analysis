#include <algorithm>
#include <fstream>
#include <functional>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>

// Read clauses from file
static int readClauses(std::vector<std::vector<int>>& clauses, int& numVars, int& numClauses, const std::string& inputFileStr) {
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
	std::vector<int> clause;
	while (std::getline(file, lineStr)) {
		if (lineStr.size() == 0) continue; // Skip empty lines
	
		std::stringstream line(lineStr);
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


static void computeCVR(double& cvr, int numClauses, int numVars) {
	cvr = numClauses / static_cast<double>(numVars);
}

// Optimizing resolvability computation - this is asymptotically slower?
// O(m^2 n^2 log(n)) 
static int computeResolvable(long& numResolvable, long& numMergeable, std::vector<std::vector<int>>& clauses, int numVariables) {
	const auto variableComparator = [](int a, int b) {
		return std::abs(a) < std::abs(b);
	};

	// Sort variables
	// O(m n log(n))
	for (std::vector<int>& clause : clauses) {
		std::sort(clause.begin(), clause.end(), variableComparator);
	}

	// Generate clause lookup table
	// O(m n)
	std::vector<std::vector<unsigned int>> posClauseIndices(numVariables);
	std::vector<std::vector<unsigned int>> negClauseIndices(numVariables);
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

	// Find all clauses which resolve on a variable
	// O(m^2 n^2 log(n))
	for (int i = 0; i < numVariables; ++i) {
		const std::vector<unsigned int>& posClauses = posClauseIndices[i];
		const std::vector<unsigned int>& negClauses = negClauseIndices[i];
		
		// Check for clauses which resolve on the variable
		// O(m^2 n log(n))
		for (unsigned int c_i : posClauses) {
			const std::vector<int>& posClause = clauses[c_i];

			// Initialize set for checking resolvability
			// O(n log(n))
			std::set<int> found;
			for (int var : posClause) {
				found.insert(var);
			}

			// Check if any of the negative clause resolves with the positive clause
			// O(m n log(n))
			for (unsigned int c_j : negClauses) {
				const std::vector<int>& negClause = clauses[c_j];

				// Check for resolvable/mergeable clauses
				// O(n log(n))
				bool resolvable = false;
				long tmpNumMergeable = 0;
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

				// Update counts
				// O(1)
				if (resolvable) {
					numResolvable += 1;
					numMergeable  += tmpNumMergeable;
				}
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

static int writeFile(const std::string& outputFileStr, std::function<void(std::ofstream&)> writerFunc) {
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

static void writeCVR(std::ofstream& outFile, double cvr) {
	outFile << cvr << std::endl;
}

static void writeResolvability(std::ofstream& outFile, int numResolvable, int numMergeable) {
	outFile << numResolvable << " " << numMergeable << std::endl;
}

static void writeDegreeVector(std::ofstream& outFile, std::vector<int>& degreeVector) {
	for (unsigned int i = 0; i < degreeVector.size(); ++i) {
		outFile << i + 1 << " " << degreeVector[i] << std::endl;
	}
}

using namespace std::placeholders;
int main (const int argc, const char* const * argv) {
	// Validate input
	if (argc < 2) {
		std::cerr << "Usage: " << argv[0] << " <INPUT [INPUTS...]>" << std::endl;
		return 1;
	}

	int argIndex = 1;

	while (argIndex != argc) {
		// Read clauses from file
		static const std::string CNF_EXTENSION = ".cnf";
		const std::string inputFileStr(argv[argIndex]);
		const std::string inputFileBaseStr = inputFileStr.substr(0, inputFileStr.size() - CNF_EXTENSION.size());
		int numVars = 0, numClauses = 0;
		std::vector<std::vector<int>> clauses;
		if (readClauses(clauses, numVars, numClauses, inputFileStr)) return 1;

		// Calculate and output CVR
		{
			double cvr = 0;
			computeCVR(cvr, numClauses, numVars);
			writeFile(inputFileBaseStr + ".cvr", std::bind(writeCVR, _1, cvr));
		}

		// Calculate and output degree vector
		{
			std::vector<int> degreeVector(numVars);
			computeDegreeVector(degreeVector, clauses);
			writeFile(inputFileBaseStr + ".dv",  std::bind(writeDegreeVector, _1, degreeVector));
		}

		// Calculate and output num resolvable and num mergeable
		{
			long numResolvable = 0, numMergeable = 0;
			computeResolvable(numResolvable, numMergeable, clauses, numVars);
			writeFile(inputFileBaseStr + ".rvm", std::bind(writeResolvability, _1, numResolvable, numMergeable));
		}

		++argIndex;
	}

	return 0;
}
