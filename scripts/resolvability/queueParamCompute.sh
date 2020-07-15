#!/bin/bash

(
	find /scratch/ianli/parameters_of_industiral/crafted/ -name "*.cnf"
	find /scratch/ianli/parameters_of_industiral/crypto/ -name "*.cnf"
	find /scratch/ianli/parameters_of_industiral/random/ -name "*.cnf"
	find /scratch/ianli/parameters_of_industiral/verification/ -name "*.cnf"
) | while read LINE; do
	OUTFILE="${LINE%.cnf}.cmp.sh"
	cp sbatchBaseFile.sh "${OUTFILE}"
	echo "#SBATCH --output=${LINE%.cnf}.cmp.log" >> "${OUTFILE}"
	echo "time /home/jt2chung/sha1-unsat/CDCL-proof-structural-analysis/scripts/resolvability/countResolvable ${LINE}" >> "${OUTFILE}"
	chmod +x "${OUTFILE}"
	echo "${LINE%.cnf}"
	sbatch $OUTFILE
	sleep 2
done
