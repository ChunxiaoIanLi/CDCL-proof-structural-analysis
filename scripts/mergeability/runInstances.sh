#!/bin/sh

SHARCNET_ACCOUNT_NAME="vganesh"
SHARCNET_TIMEOUT="00:00:5000"
SHARCNET_MEMORY="10G"

# validate input
if [[ $# -ne 2 ]]; then
	echo "Usage: $0 <DIRECTORY> <SAT_SOLVER>"
	exit 1
fi

MAIN_DIR="${1%/}"
SAT_SOLVER="$2"

# run merge instances
runinstance() {
	INSTANCE_NAME="${1%.cnf}"
	echo "Queuing SAT solving for ${1}"

	# create script to generate merge instances
	JOB_SCRIPT="${INSTANCE_NAME}.sh"
	echo "#!/bin/bash" > ${JOB_SCRIPT}
	echo "#SBATCH --account=def-${SHARCNET_ACCOUNT_NAME}" >> ${JOB_SCRIPT}
	echo "#SBATCH --time=${SHARCNET_TIMEOUT}" >> ${JOB_SCRIPT}
	echo "#SBATCH --mem=${SHARCNET_MEMORY}" >> ${JOB_SCRIPT}
	echo "#SBATCH --job-name=runMerge" >> ${JOB_SCRIPT}
	echo "#SBATCH --output=${INSTANCE_NAME}.log" >> ${JOB_SCRIPT}

	# generate merge instances
	OUTPUT_INSTANCE_PREFIX="outputInstance"
	echo "${SAT_SOLVER} \"${1}\"" >> ${JOB_SCRIPT}

	# queue job
	sbatch ${JOB_SCRIPT}

	# Wait between queuing jobs
	sleep 2
}

shopt -s extglob

# iterate over all CNF files
find ${MAIN_DIR} -name '*.cnf' | while read -r CNF_FILE ; do
	runinstance "${CNF_FILE}"
done
