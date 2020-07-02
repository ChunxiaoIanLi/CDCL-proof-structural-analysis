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
static int readClauses(std::vector<std::vector<int>>& clauses, int& numVars, int& numClauses, const std::string& inputFileStr) {
	std::ifstream file(inputFileStr);
	if (!file.is_open()) {
		std::cerr << "Error while opening: " << inputFileStr << std::endl;
		return 1;
	}

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


static void computeCVR(double& cvr, int numClauses, int numVars) {
	cvr = numClauses / static_cast<double>(numVars);
}

// Resolvability computation
// O(m^2 n log(n))
static int computeResolvable1(int& numResolvable, int& numMergeable, const std::vector<std::vector<int>>& clauses) {
	for (unsigned int i = 0; i < clauses.size(); ++i) {
		// Initialize set for checking resolvability
		// O(n log(n))
		std::set<int> found;
		for (unsigned int c_i = 0; c_i < clauses[i].size(); ++c_i) {
			found.insert(clauses[i][c_i]);
		}

		// Compare every clause with every other clause
		// O(m n log(n))
		for (unsigned int j = i + 1; j < clauses.size(); ++j) {
			bool resolvable = false;
			long tmpNumMergeable = 0;
			
			// Check for resolvable/mergeable clauses
			// O(n log(n))
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
			// O(1)
			if (resolvable) {
				numResolvable += 1;
				numMergeable  += tmpNumMergeable;
			}
		}
	}

	return 0;
}

// Optimization of resolvability computation - this is over-counting! D:
// Still O(m^2 n log(n)), but faster than computeResolvable
static int computeResolvable2(int& numResolvable, int& numMergeable, std::vector<std::vector<int>>& clauses) {
	const auto variableComparator = [](int a, int b) {
		return std::abs(a) < std::abs(b);
	};
	const auto clauseComparator = [](const std::vector<int>& a, const std::vector<int>& b) {
		return std::abs(a[0]) < std::abs(b[0]);
	};

	// Sort variables
	// O(m n log(n))
	for (std::vector<int>& clause : clauses) {
		std::sort(clause.begin(), clause.end(), variableComparator);
	}

	// Sort clauses
	// O(m log(m))
	std::sort(clauses.begin(), clauses.end(), clauseComparator);

	// Calculate resolvability and mergeability
	// O(m^2 n log(n))
	// Iterate through each variable of each clause
	for (unsigned int i = 0; i < clauses.size(); ++i) {
		// Initialize set for checking resolvability
		// O(n log(n))
		std::set<int> found;
		for (unsigned int c_i = 0; c_i < clauses[i].size(); ++c_i) {
			found.insert(clauses[i][c_i]);
		}

		// Initialize set for tracking clauses which have already been checked
		std::set<int> checked;

		// For each variable in the clause, check for other clauses which resolve on the variable
		for (unsigned int c_i = 0; c_i < clauses[i].size(); ++c_i) {
			// Find the last possibly resolvable clause ahead of the current clause
			// Since clauses are sorted, the first clause which starts with a value larger than the target variable is an upper bound
			// on the search range.
			// O(n + log(m))
			const std::vector<int> toFind = { clauses[i][c_i] }; // Wrap the target variable in a clause for comparison
			const auto resolvableUpperBound = std::upper_bound(clauses.begin() + i + 1, clauses.end(), toFind, clauseComparator);

			// Find all resolvable clauses in the range of candidates
			// O(m (log(m) + n log(n)))
			for (auto candidateClauseItr = clauses.begin(); candidateClauseItr != resolvableUpperBound; ++candidateClauseItr) {
				const std::vector<int>& candidateClause = *candidateClauseItr;				

				// Check if the desired variable is potentially in the candidate clause
				// Since variables are sorted, we can skip clauses whose maximum variables are smaller than the target variable
				// O(1)
				if (std::abs(candidateClause.back()) < std::abs(clauses[i][c_i])) continue;

				// Check whether the candidate clause has already been checked
				// O(log(m))
				const int curIndex = candidateClauseItr - clauses.begin(); 
				if (checked.find(curIndex) != checked.end()) continue;
				checked.insert(curIndex);

				// Check if the target variable is in the candidate clause
				// Since variables are sorted, the first variable less than or equal to the target variable is a lower bound
				// O(log(n))
				const auto lowerBound = std::lower_bound(candidateClause.begin(), candidateClause.end(), clauses[i][c_i], variableComparator);
				if (lowerBound == candidateClause.end()) continue; // Skip clause if no such element exists
				if (*lowerBound != -clauses[i][c_i]) continue; // Skip clause if it does not resolve on the target variable

				// Check for resolvable/mergeable clauses
				// O(n log(n))
				bool resolvable = false;
				int tmpNumMergeable = 0;
				for (unsigned int c_j = 0; c_j < candidateClause.size(); ++c_j) {
					if (found.find(-candidateClause[c_j]) != found.end()) {
						if (resolvable) {
							resolvable = false;
							break;
						}
						resolvable = true;
					} else if (found.find(candidateClause[c_j]) != found.end()) {
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
	outFile << numResolvable << " " << numMergeable << std::endl;
	return 0;
}

static int writeDegreeVector(std::ofstream& outFile, std::vector<int>& degreeVector) {
	for (unsigned int i = 0; i < degreeVector.size(); ++i) {
		outFile << i + 1 << " " << degreeVector[i] << std::endl;
	}
	return 0;
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
		const std::string inputFileStr(argv[argIndex]);
		int numVars = 0, numClauses = 0;
		std::vector<std::vector<int>> clauses;
		if (readClauses(clauses, numVars, numClauses, inputFileStr)) return 1;

		// Calculate and output CVR
		{
			double cvr = 0;
			computeCVR(cvr, numClauses, numVars);
			writeFile(inputFileStr + ".cvr", std::bind(writeCVR, _1, cvr));
		}

		// Calculate and output degree vector
		{
			std::vector<int> degreeVector(numVars);
			computeDegreeVector(degreeVector, clauses);
			writeFile(inputFileStr + ".dv",  std::bind(writeDegreeVector, _1, degreeVector));
		}

		// Calculate and output num resolvable and num mergeable
		{
			int numResolvable = 0, numMergeable = 0;
			int algNum = 2;
			switch (algNum) {
				case  2: computeResolvable2(numResolvable, numMergeable, clauses); break; 
				default: computeResolvable1(numResolvable, numMergeable, clauses); break;
			}

			writeFile(inputFileStr + ".rvm" + ((algNum == 1) ? std::string() : std::to_string(algNum)), std::bind(writeResolvability, _1, numResolvable, numMergeable));
		}

		++argIndex;
	}

	return 0;
}
