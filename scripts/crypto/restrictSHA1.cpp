#include <iostream>
#include <string>
#include <fstream>
#include <sstream>

// This script restricts n random bits in a SAT-encoded SHA1 instance

// Determine whether a string is another string's prefix
static bool isPrefix(const std::string& str, const std::string& prefix) {
    for (int i = 0; i < str.length() && i < prefix.length(); ++i) {
        if (str[i] != prefix[i]) return false;
    }

    return true;
}

// Shuffle an array
static void shuffle(int* list, int length, int shuffleFirstN) {
    for (int i = 0; i < shuffleFirstN; ++i) {
        const int indexToSwap = static_cast<int>(std::rand() / static_cast<double>(RAND_MAX) * (length - i)) + i; 
        std::swap(list[i], list[indexToSwap]);
    }
}

// Restrict the bits in a CNF encoding of a SHA1 instance
int main (int argc, char** argv) {
    const int minNumRestricted = 1;
    const int maxNumRestricted = 512;

    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <num bits to restrict> <input file> <output file>" << std::endl;
        return 1;
    }

    const int numToRestrict = atoi(argv[1]);
    if (numToRestrict < minNumRestricted || numToRestrict > maxNumRestricted) {
        std::cerr << "Must restrict between " << minNumRestricted << " and " << maxNumRestricted << " variables." << std::endl;
        return 1;
    }

    const std::string headerPrefix = "p cnf ";

    std::ifstream cnfFile(argv[2]);
    std::ofstream outfile(argv[3]);
    std::string line;
    while (std::getline(cnfFile, line)) {
        if (isPrefix(line, headerPrefix)) {
            std::istringstream iss(line.substr(headerPrefix.length()));
            int numVariables = 0;
            int numClauses = 0;
            if (!(iss >> numVariables >> numClauses)) {
                return 1;
            }

            outfile << headerPrefix << numVariables << " " << numClauses + numToRestrict << std::endl;
        } else {
            outfile << line << std::endl;
        }
    }

    // Randomly set n bits
    const int totalNumBits = 512;
    int randomizedOrder[totalNumBits];
    for (int i = 0; i < totalNumBits; ++i) {
        randomizedOrder[i] = i;
    }

    shuffle(randomizedOrder, totalNumBits, numToRestrict);
    for (int i = 0; i < numToRestrict; ++i) {
        const int sign = (std::rand() & 0b1) ? (1) : (-1);
        outfile << sign * (randomizedOrder[i] + 1) << " " << 0 << std::endl;
    }

    return 0;
}