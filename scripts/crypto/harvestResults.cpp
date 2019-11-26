#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <regex>
#include <vector>

// This script generates a CSV for the results of queue_experiments.sh

 enum class Satisfiability {
    SAT,
    UNSAT,
    UNKNOWN,
};

struct GlucoseResults {
    bool m_timedOut = false;
    double m_timeElapsed = 0;
    int m_numVariables = 0;
    int m_numClauses = 0;
    Satisfiability m_satisfiability = Satisfiability::UNKNOWN;
};

enum class GlucoseSearchState {
    SEARCH_VARIABLES,
    SEARCH_CLAUSES,
    SEARCH_TIME,
    SEARCH_SATISIFIABILITY,
    COMPLETE,
};

GlucoseResults getResultsForFile(const std::string& filename) {
    GlucoseResults results{};
    std::ifstream resultsFile(filename);
    std::string line;
    std::getline(resultsFile, line);
    if (line.find("DUE TO TIME LIMIT") != std::string::npos) {
        results.m_timedOut = true;
        return results;
    }

    GlucoseSearchState currentSearchState = GlucoseSearchState::SEARCH_VARIABLES;
    while (std::getline(resultsFile, line) && currentSearchState != GlucoseSearchState::COMPLETE) {
        switch (currentSearchState) {
            case GlucoseSearchState::SEARCH_VARIABLES: {
                if (line.find("Number of variables") != std::string::npos) {
                    std::istringstream iss(line.substr(line.find_first_of(":") + 1));
                    if (!(iss >> results.m_numVariables)) {
                        break;
                    }
                    currentSearchState = GlucoseSearchState::SEARCH_CLAUSES;
                }
            } break;
            case GlucoseSearchState::SEARCH_CLAUSES: {
                if (line.find("Number of clauses") != std::string::npos) {
                    std::istringstream iss(line.substr(line.find_first_of(":") + 1));
                    if (!(iss >> results.m_numClauses)) {
                        break;
                    }
                    currentSearchState = GlucoseSearchState::SEARCH_TIME;
                }
            } break;
            case GlucoseSearchState::SEARCH_TIME: {
                if (line.find("CPU time") != std::string::npos) {
                    std::istringstream iss(line.substr(line.find_first_of(":") + 1));
                    if (!(iss >> results.m_timeElapsed)) {
                        break;
                    }
                    currentSearchState = GlucoseSearchState::SEARCH_SATISIFIABILITY;
                }
            } break;
            case GlucoseSearchState::SEARCH_SATISIFIABILITY: {
                if (line.find("SATISFIABLE") != std::string::npos) {
                    if (line.find("UNSATISFIABLE") != std::string::npos) {
                        results.m_satisfiability = Satisfiability::UNSAT;
                    } else {
                        results.m_satisfiability = Satisfiability::SAT;
                    }
                    currentSearchState = GlucoseSearchState::COMPLETE;
                }
            } break;
            default: return results;
        }
    }

    return results;
}

int main (int argc, char** argv) {
    if (argc != 7) {
        std::cerr << "Usage: " << argv[0] << " <input directory> <begin rounds> <end rounds> <begin restrictions> <end restrictions> <output file>" << std::endl;
        return 1;
    }

    const int beginRounds = atoi(argv[2]);
    const int endRounds = atoi(argv[3]);
    const int beginRestrictions = atoi(argv[4]);
    const int endRestrictions = atoi(argv[5]);

    if (beginRounds > endRounds) {
        std::cerr << "Cannot begin rounds after end" << std::endl;
        return 1;
    }

    if (beginRestrictions > endRestrictions) {
        std::cerr << "Cannot begin restrictions after end" << std::endl;
        return 1;
    }

    char buf[512];
    std::ofstream outfile(argv[6]);
    outfile << "Rounds, Restrictions, Variables, Clauses, Timed Out, Running Time, Satisfiability" << std::endl;

    for (int i = beginRounds; i <= endRounds; ++i) {
        for (int j = beginRestrictions; j <= endRestrictions; ++j) {
            memset(buf, '\0', sizeof(buf));
            sprintf(buf, "%s/%d_rounds/%d_restrictions/%d_%d_SHA1_output.txt", argv[1], i, j, i, j);
            GlucoseResults results = getResultsForFile(buf);

            outfile
                << i << ","
                << j << ","
                << results.m_numVariables << ","
                << results.m_numClauses << ","
                << results.m_timedOut << ","
                << results.m_timeElapsed << ","
                << ((results.m_satisfiability == Satisfiability::SAT)
                    ? "SAT" : (results.m_satisfiability == Satisfiability::UNSAT)
                    ? "UNSAT"
                    : "UNKNOWN")
                << std::endl;
        }
    }

    return 0;
}