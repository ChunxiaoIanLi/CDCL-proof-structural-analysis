#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#define MAX_LINE_SIZE 2048

// Read clauses from file
static int readClauses(std::vector<std::vector<int>>& clauses, std::ifstream& file) {
	char buffer[MAX_LINE_SIZE];

	// Read CNF header
	bool gotHeader = false;
	while (!gotHeader) {
		file.getline(buffer, MAX_LINE_SIZE);
		if (file.bad()) return 1;
		std::string bufferStr(buffer);
		if (bufferStr.size() == 0) continue; // Skip empty lines

		std::stringstream line(bufferStr);
		char firstChar = 0;
		line >> firstChar;
		if (firstChar == 'c') continue;	// Handle comments
		if (firstChar != 'p') {
			std::cerr << "Could not find header line" << std::endl;
			return 1;
		}

	}

	// Read clauses
	while (file.good()) {
		int var = 0;
		file >> var;
		if (file.bad()) return 1;
		std::cout << var << std::endl;
	}
	return 0;
}

static int countResolvable(int& numResolvable, int& numMergeable, const std::vector<std::vector<int>>& clauses) {
	return 0;
}

int main (const int argc, const char* const * argv) {
	if (argc < 3) {
		std::cerr << "Usage: " << argv[0] << " <OUTPUT> <INPUT [INPUTS...]>" << std::endl;
		return 1;
	}

	std::cout << "Okay!" << std::endl;

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
		if (!countResolvable(numResolvable, numMergeable, clauses)) {
			std::cerr << "Error while counting num resolvable for: " << inputFileStr << std::endl;
			return 1;
		}

		// Write results to file
		outputFile <<
			inputFileStr << ',' <<
			numResolvable << ',' <<
			numMergeable << ',' <<
		std::endl;

		++argIndex;
	}

	return 0;
}
