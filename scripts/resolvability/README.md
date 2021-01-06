# Scripts
This directory contains a variety of scripts for running jobs related to resolvability.

## queueArrayJob.sh
This script generates a script for queuing and running an array of jobs based on entries in a file. This is intended to be used for computing parameters and running SAT solvers over CNF instances.

Usage: ./queueArrayJob.sh <INPUT_FILE> <START_INDEX> <NUM_LINES>
- <INPUT_FILE> refers to the file over which to run jobs. This should be used to store the list of CNF files.
- <START_INDEX> this is the line number of the line to start at.
- <NUM_LINES> this is the number of instances to run.

## PMILib.py
This is a python library for computing resolvability and mergeability parameters. This makes use of pythonBindings.cpp and the code under the src/ directory, using libmergeability.so.

## main.cpp
This script is used for computing the CVR, degree vector, resolvability, and mergeability over CNF instances.

# make
This compiles the code for main.cpp into an executable: countResolvable

# make python
This compiles the code for the python library: libmergeability.so, which is needed for PMILib.py.

## queueParamCompute.sh
This script is used for queuing jobs for computing the CVR, degree vector, resolvability, and mergeability over CNF instances using main.cpp. This script's functionality is made redundant by queueArrayJob.sh.

## runInstances.sh
This script is used for queuing jobs for running SAT solvers over CNF instances. This script's functionality is made redundant by queueArrayJob.sh.

Usage: ./runInstances.sh <SAT_SOLVER> <CNF_FILE [...]>
- <SAT_SOLVER> this is the path to the SAT solver to use to solve CNF files
- <CNF_FILE [...]> this is a list of all the CNF files to solve

## generateCSV.sh
This script is used for collecting the information generated by running the queueParamCompute.sh and runInstances.sh scripts.