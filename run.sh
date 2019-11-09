#!/bin/bash

path=$1
file=$2

/home/ianli/CDCL-proof-structural-analysis/executables/glucose $path/$file -certified -certified-output=/scratch/ianli/DRUPproof/$file.drup > /scratch/ianli/glucoseResult/$file.glucose

/home/ianli/CDCL-proof-structural-analysis/executables/drat-trim $path/$file /scratch/ianli/DRUPproof/$file.drup -l /scratch/ianli/DRATcore/$file.core.drat

/home/ianli/CDCL-proof-structural-analysis/executables/drat-trim $path/$file /scratch/ianli/DRATcore/$file.core.drat -r /scratch/ianli/coreDependency/$file.dependency

python /home/ianli/CDCL-proof-structural-analysis/scripts/dependencyToGR.py /scratch/ianli/coreDependency/ $file.dependency


