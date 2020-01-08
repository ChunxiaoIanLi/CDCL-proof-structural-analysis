#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include <vector>

std::unique_ptr<std::vector<std::vector<int>>> getMigClauses(const std::vector<std::vector<int>>& clauses) {
    // Naive merge check
    const int SHARES_LIT = 0x1 << 0;
    const int SHARES_NEG = 0x1 << 1;
    const int MERGY = SHARES_LIT | SHARES_NEG;

    std::unique_ptr<std::vector<std::vector<int>>> migClauses = std::make_unique<std::vector<std::vector<int>>>();

    for (unsigned int ci = 0; ci < clauses.size(); ++ci) {
        const std::vector<int>& c1 = clauses[ci];
        for (unsigned int cj = ci + 1; cj < clauses.size(); ++cj) {
            const std::vector<int>& c2 = clauses[cj];

            // Check if clauses are mergy
            int shareState = 0;
            for (int vi = 0; vi < c1.size() && shareState != MERGY; ++vi) {
                for (int vj = 0; vj < c2.size() && shareState != MERGY; ++vj) {
                    if (c1[vi] == c2[vj]) {
                        shareState |= SHARES_LIT;
                    } else if (c1[vi] == -c2[vj]) {
                        shareState |= SHARES_NEG;
                    }
                }
            }

            // Add a MIG clause if the CNF clauses are mergy
            if (shareState == MERGY) {
                migClauses->push_back(std::vector<int>{static_cast<int>(ci), static_cast<int>(cj)});
            }
        }
    }

    return migClauses;
}

int main (int argc, char** argv) {
    // Input validation
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <INPUT_CNF> <OUTPUT_MIG>" << std::endl;
        return EXIT_FAILURE;
    }

    // Open file
    std::fstream cnfFileStream(argv[1]);

    int numVars = -1;
    int numClauses = -1;
    std::vector<std::vector<int>> clauses{};

    // Read file
    std::string line;
    while (std::getline(cnfFileStream, line)) {
        char firstChar = line[0];

        // Skip comment lines
        if (firstChar == 'c') {
            continue;

        // Initialize from header line
        } else if (firstChar == 'p') {
            if (numVars == -1 && numClauses == -1) {
                std::istringstream headerLine(line);
                headerLine >> firstChar;
                if (!(headerLine >> numVars >> numClauses) || numVars == -1 || numClauses == -1) {
                    std::cerr << "Could not initialize from header line: \"" << line << "\"" << std::endl;
                    return EXIT_FAILURE;
                };
            } else {
                std::cerr << "Found multiple header lines in file: " << argv[1] << std::endl;
                return EXIT_FAILURE;
            }

        // Read clause
        } else {
            std::vector<int> clause;
            std::istringstream clauseLine(line);
            int literal = 0;
            do {
                if (!(clauseLine >> literal)) {
                    std::cerr << "Could not read literal from clause line: \"" << line << "\"" << std::endl;
                    return EXIT_FAILURE;
                } else if (literal) {
                    clause.push_back(literal);
                }
            } while (literal);
            clauses.push_back(std::move(clause));
        }
    }

    // Get mergy clauses
    std::unique_ptr<std::vector<std::vector<int>>> migClauses = getMigClauses(clauses);

    // Open output file
    FILE* migFile = fopen(argv[2], "w");
    if (migFile == nullptr) {
        std::cerr << "Could not open output file: \"" << argv[2] << "\"" << std::endl;
        return EXIT_FAILURE;
    }

    fprintf(migFile, "p tw %u %lu\n", numClauses, migClauses->size());

    // Output MIG clauses
    for (int i = 0; i < migClauses->size(); ++i) {
        const std::vector<int>& clause = (*migClauses)[i];
        for (int j = 0; j < clause.size(); ++j) {
            fprintf(migFile, "%d ", clause[j] + 1);
        }
        fprintf(migFile, "0\n");
    }

    fclose(migFile);

    std::cout << "Conversion finished!" << std::endl;
    return EXIT_SUCCESS;
}