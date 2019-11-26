#!/bin/bash

#./run.sh path_to_directory file_name full_path_to_treewidth_solver

path=$1
file=$2
twsolver=$3

# CPU and RAM info
echo
echo "CPU information:"
echo $(lscpu)

echo
echo "RAM information:"
echo $(free -m)

# Glucose solving
echo
echo solving
echo

start=$(($(date +%s%N)/1000000))

~/CDCL-proof-structural-analysis/executables/glucose $path/$file -certified -certified-output=~/scratch/DRUPproof/$file.drup > ~/scratch/glucoseResult/$file.glucose

end=$(($(date +%s%N)/1000000))

diff=$(($end-$start))

echo
echo "Glucose executed in:" + $diff + "milliseconds"
echo

# Drat core computation
echo
echo computing DRAT core
echo

start=$(($(date +%s%N)/1000000))

~/CDCL-proof-structural-analysis/executables/drat-trim $path/$file ~/scratch/DRUPproof/$file.drup -l ~/scratch/DRATcore/$file.core.drat

end=$(($(date +%s%N)/1000000))

diff=$(($end-$start))

echo
echo "Core computation executed in:" + $diff + "milliseconds"
echo

# Drat-trim dependency computation
echo
echo computing dependency of DRAT \in TraceCheck format
echo

start=$(($(date +%s%N)/1000000))

~/CDCL-proof-structural-analysis/executables/drat-trim $path/$file ~/scratch/DRATcore/$file.core.drat -r /scratch/ianli/coreDependency/$file.dependency

end=$(($(date +%s%N)/1000000))

diff=$(($end-$start))

echo
echo "Dependency computation executed in:" + $diff + "milliseconds"
echo

# .gr conversion
echo
echo converting TraceCheck to .gr format
echo

start=$(($(date +%s%N)/1000000))

python ~/CDCL-proof-structural-analysis/scripts/dependencyToGR.py ~/scratch/coreDependency/ $file.dependency

end=$(($(date +%s%N)/1000000))

diff=$(($end-$start))

echo
echo ".gr conversion executed in:" + $diff + "milliseconds"
echo

echo
echo computing tree decomposition
echo

$twsolver ~/scratch/coreGR/$file.dependency.gr > ~/scratch/treeDecomposition/$file.decomposition
