#!/bin/bash

MAX_RETRIES=3;

(
	find /scratch/ianli/parameters_of_industiral/ -name "*.cnf"
) | while read LINE; do
	OUTFILE="${LINE%.cnf}.cmp.sh"
	cp sbatchBaseFile.sh "${OUTFILE}"
	echo "#SBATCH --output=${LINE%.cnf}.cmp.log" >> "${OUTFILE}"
	echo "time /home/jt2chung/sha1-unsat/CDCL-proof-structural-analysis/scripts/resolvability/countResolvable -a ${LINE}" >> "${OUTFILE}"
	chmod +x "${OUTFILE}"
	echo "${LINE%.cnf}"
	for (( i=0; i <= ${MAX_RETRIES}; ++i )); do
		if sbatch $OUTFILE; then
			break
		else
			echo "Retrying... $((i + 1))/${MAX_RETRIES}"
		fi
	done
	sleep 2
done
