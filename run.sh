#!/bin/bash

#./run.sh path_to_directory file_name full_path_to_treewidth_solver

path=$1
file=$2
twsolver=$3

echo
echo solving
echo

~/CDCL-proof-structural-analysis/executables/glucose $path/$file -certified -certified-output=~/scratch/DRUPproof/$file.drup > ~/scratch/glucoseResult/$file.glucose

echo
echo computing DRAT core
echo

~/CDCL-proof-structural-analysis/executables/drat-trim $path/$file ~/scratch/DRUPproof/$file.drup -l ~/scratch/DRATcore/$file.core.drat

echo
echo computing dependency of DRAT \in TraceCheck format
echo

~/CDCL-proof-structural-analysis/executables/drat-trim $path/$file ~/scratch/DRATcore/$file.core.drat -r /scratch/ianli/coreDependency/$file.dependency

echo
echo converting TraceCheck to .gr format
echo

python ~/CDCL-proof-structural-analysis/scripts/dependencyToGR.py ~/scratch/coreDependency/ $file.dependency

echo
echo computing tree decomposition
echo

$twsolver ~/scratch/coreGR/$file.dependency.gr > ~/scratch/treeDecomposition/$file.decomposition
