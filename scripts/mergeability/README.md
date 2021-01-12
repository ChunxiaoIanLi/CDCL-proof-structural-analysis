# Scripts
This directory contains a variety of scripts for running jobs related to mergeability.

## runMergeGen.sh
Generate instances with different mergeabilities based on an input CNF instance. 

Usage: ./runMergeGen.sh <DIRECTORY> <INSTANCES_CSV> <NUM_TO_EXECUTE> <INTERMEDIATE_FLIPS> <MAX_FLIPS>
- <DIRECTORY> this is the directory which contains all the input CNFs
- <INSTANCES_CSV> this file contains a list of all the instances to use
- <NUM_TO_EXECUTE> the number of CNF files to output per input file
- <INTERMEDIATE_FLIPS> the step size to use when incrementing the number of flips
- <MAX_FLIPS> the number of flips at which to stop incrementing

## runInstances.sh
DEPRECATED
Queue jobs to run a SAT solver on CNF instances

Usage: ./runInstances.sh <DIRECTORY> <SAT_SOLVER>
- <DIRECTORY> this is the directory which contains all the input CNFs
- <SAT_SOLVER> this is the SAT solver to use to run the instances

## runMerge.sh
DEPRECATED
Queue jobs to calculate the mergeability of CNF instances using Ed's scripts

Usage: ./runMerge.sh <DIRECTORY> <MERGE_COMPILED>
- <DIRECTORY> this is the directory which contains all the input CNFs
- <MERGE_COMPILED> this is the tool used to run the instances

## getInstances.sh
DEPRECATED
Get the CVR, instance type, and SAT solver results from CNF instances and store them in a CSV.

Usage: ./getInstances.sh <DIRECTORY> <OUTPUT_FILE>
- <DIRECTORY> this is the directory which contains all the input CNFs
- <OUTPUT_FILE> this is the name of the file to output

## generateMergeInstances.sh
DEPRECATED
Queue jobs to generate merge instances based on input CNF instances

Usage: ./generateMergeInstances.sh <DIRECTORY> <INSTANCES_CSV> <NUM_TO_EXECUTE> <OUT_DIRECTORY> <MERGE_GENERATOR>
- <DIRECTORY> this is the directory which contains all the input CNFs
- <INSTANCES_CSV> this is the output of getInstances.sh
- <NUM_TO_EXECUTE> this is the number of instances to run merge generation on
- <OUT_DIRECTORY> this is the directory into which to write the output instances
- <MERGE_GENERATOR> this is the tool used to generate new instances from input CNFs
