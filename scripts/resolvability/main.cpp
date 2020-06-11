#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>

#define MAX_LINE_SIZE 2048
#define RESOLVABLE_SHIFT 1
#define MERGEABLE_SHIFT 2
#define RESOLVABLE_MASK (0x1 << RESOLVABLE_SHIFT)
#define MERGEABLE_MASK (0x1 << MERGEABLE_SHIFT)

// Read clauses from file
static int readClauses(std::vector<std::vector<int>>& clauses, std::ifstream& file) {
	char buffer[MAX_LINE_SIZE];

	// Read CNF header
	bool gotHeader = false;
	int numVars = 0, numClauses = 0;
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

// O(n) in size of clauses
// Resolvable if there is exactly 1 resolving literal
// Mergeable if there is at least 1 common literal AND the pair is resolvable
static int getResolvable(const std::vector<int>& c1, const std::vector<int>& c2) {
	int resolvable = 0, mergeable = 0;
	std::set<int> found;
	for (unsigned int i = 0; i < c1.size(); ++i) {
		found.insert(c1[i]);
	}

	for (unsigned int i = 0; i < c2.size(); ++i) {
		if (found.find(-c2[i]) != found.end()) {
			if (resolvable) return 0; // Not mergeable and not resolvable if there are multiple resolving literals
			resolvable = 1;
		}
		if (found.find(+c2[i]) != found.end()) {
			mergeable = 1;
		}
	}

	return (resolvable << RESOLVABLE_SHIFT) || (mergeable << MERGEABLE_SHIFT);
}

static int countResolvable(int& numResolvable, int& numMergeable, const std::vector<std::vector<int>>& clauses) {
	for (unsigned int i = 0; i < clauses.size(); ++i) {
		for (unsigned int j = i + 1; j < clauses.size(); ++j) {
			int val = getResolvable(clauses[i], clauses[j]);
			if (val & RESOLVABLE_MASK) ++numResolvable;
			if (val & MERGEABLE_MASK) ++numMergeable;
		}
	}

	return 0;
}

int main (const int argc, const char* const * argv) {
	if (argc < 3) {
		std::cerr << "Usage: " << argv[0] << " <OUTPUT> <INPUT [INPUTS...]>" << std::endl;
		return 1;
	}

	int argIndex = 1;
	const std::string outputFileStr(argv[argIndex++]);
	std::ofstream outputFile(outputFileStr);
	if (outputFile.bad()) {
		std::cerr << "Error while opening: " << outputFileStr << std::endl;
		return 1;
	}

	while (argIndex != argc) {
		// Open file
		const std::string inputFileStr(argv[argIndex]);
		std::ifstream inputFile(inputFileStr);
		if (inputFile.bad()) {
			std::cerr << "Error while opening: " << inputFileStr << std::endl;
			return 1;
		}

		// Read clauses from file
		std::vector<std::vector<int>> clauses;
		if (readClauses(clauses, inputFile)) {
			std::cerr << "Error while reading: " << inputFileStr << std::endl;
			return 1;
		}

		// Calculate num resolvable and num mergeable
		int numResolvable = 0, numMergeable = 0;
		if (countResolvable(numResolvable, numMergeable, clauses)) {
			std::cerr << "Error while counting num resolvable for: " << inputFileStr << std::endl;
			return 1;
		}

		// Write results to file
		std::cout  << inputFileStr << ',' << numResolvable << ',' << numMergeable << ',' << std::endl;
		outputFile << inputFileStr << ',' << numResolvable << ',' << numMergeable << ',' << std::endl;

		++argIndex;
	}

	return 0;
}
