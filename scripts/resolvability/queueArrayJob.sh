# Input validation
if [[ $# -ne 3 ]]; then
	echo "Usage: $0 <INPUT_FILE> <START_INDEX> <NUM_LINES>"
	exit
fi

# Set up parameters
INPUT_FILE=$1
START_INDEX=$2
END_INDEX=$((START_INDEX + $3 - 1))
SCRIPT_FILE="arrayJobScript.sh"

# Compute hierarchical parameters
#SCRIPT="python /home/jt2chung/sha1-unsat/CDCL-proof-structural-analysis/hierarchical_community_structure/clustering_ed.py \${INSTANCE_NAME}"

# Compute degree vector
#SCRIPT="/home/jt2chung/sha1-unsat/CDCL-proof-structural-analysis/scripts/resolvability/countResolvable -d \${INSTANCE_NAME}"

# Run SAT solver
SCRIPT="/home/jt2chung/sha1-unsat/maplesat_static -cpu-lim=4950 \"\${INSTANCE_NAME}\" > \"\${INSTANCE_NAME}.log\""

# Generate script for sbatch
echo "#!/bin/bash"                                                              > "${SCRIPT_FILE}"
echo "#SBATCH --account=def-vganesh"                                           >> "${SCRIPT_FILE}"
echo "#SBATCH --time=0:00:5000"                                                >> "${SCRIPT_FILE}"
echo "#SBATCH --mem=10G"                                                       >> "${SCRIPT_FILE}"
echo "#SBATCH --array=${START_INDEX}-${END_INDEX}"                             >> "${SCRIPT_FILE}"
echo "#SBATCH --exclude=gra[801-1325]"                                         >> "${SCRIPT_FILE}"
echo ""                                                                        >> "${SCRIPT_FILE}"
echo "echo \"Using node \${SLURMD_NODENAME} for job \${SLURM_ARRAY_TASK_ID}\"" >> "${SCRIPT_FILE}"
echo "source /home/jt2chung/sat/bin/activate"                                  >> "${SCRIPT_FILE}"
echo "INSTANCE_NAME=\`sed -n \${SLURM_ARRAY_TASK_ID}p ${INPUT_FILE}\`"         >> "${SCRIPT_FILE}"
echo "${SCRIPT}"                                                               >> "${SCRIPT_FILE}"

# Queue script
sbatch ${SCRIPT_FILE}
