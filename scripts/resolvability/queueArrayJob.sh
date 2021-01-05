# Input validation
if [[ $# -ne 3 ]]; then
	echo "Usage: $0 <INPUT_FILE> <START_INDEX> <NUM_LINES>"
	exit
fi

# Set up parameters
INPUT_FILE=$1
START_INDEX=$2
END_INDEX=$((START_INDEX + $3))
SCRIPT_FILE="arrayJobScript.sh"
#SCRIPT="/home/jt2chung/sha1-unsat/CDCL-proof-structural-analysis/scripts/resolvability/countResolvable -d \${INSTANCE_NAME}"
SCRIPT="/home/jt2chung/sha1-unsat/maplesat_static -cpu-lim=4950 \"\${INSTANCE_NAME}\" > \"\${INSTANCE_NAME%.cnf}.log\""

# Generate script for sbatch
echo "#!/bin/bash"                                                         > "${SCRIPT_FILE}"
echo "#SBATCH --account=def-vganesh"                                      >> "${SCRIPT_FILE}"
echo "#SBATCH --time=0:00:5000"                                           >> "${SCRIPT_FILE}"
echo "#SBATCH --mem=5G"                                                   >> "${SCRIPT_FILE}"
echo "#SBATCH --job-name=countRes"                                        >> "${SCRIPT_FILE}"
echo "#SBATCH --array=${START_INDEX}-${END_INDEX}"                        >> "${SCRIPT_FILE}"
echo ""                                                                   >> "${SCRIPT_FILE}"
echo "RANGE_START=\$((SLURM_ARRAY_TASK_ID + 1))"                          >> "${SCRIPT_FILE}"
echo "RANGE_END=\$((RANGE_START + 99))"                                   >> "${SCRIPT_FILE}"
echo "RANGE_END_PLUS=\$((RANGE_END + 1))"                                 >> "${SCRIPT_FILE}"
echo "SED_QUERY=\"\${RANGE_START},\${RANGE_END}p;\${RANGE_END_PLUS}q;d\"" >> "${SCRIPT_FILE}"
echo "INSTANCE_NAME=\`sed \${SED_QUERY} ${INPUT_FILE}\`"                  >> "${SCRIPT_FILE}"
echo "${SCRIPT}"                                                          >> "${SCRIPT_FILE}"

# Queue script
sbatch ${SCRIPT_FILE}
