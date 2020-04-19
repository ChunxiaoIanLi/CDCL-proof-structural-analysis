#!/bin/sh

SHARCNET_ACCOUNT_NAME="vganesh"
SHARCNET_TIMEOUT="01:00:00"
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

INSTANCE_TYPES=("medium" "powerlaw" "uniform")

# iterate over all ratios
ls "${MAIN_DIR}" | grep "ratio" | while read -r INNER ; do
	SUB_DIR="${MAIN_DIR}/${INNER}/instances"

	# iterate over all instance types
	for INSTANCE_TYPE in "${INSTANCE_TYPES[@]}"; do
		SUBSUB_DIR="${SUB_DIR}/${INSTANCE_TYPE}"
	
		# iterate over all base instances
		if [[ -r "${SUBSUB_DIR}" ]]; then
			ls "${SUBSUB_DIR}" | while read -r BASE_INSTANCE ; do
				SUBSUBSUB_DIR="${SUBSUB_DIR}/${BASE_INSTANCE}"

			# iterate over all instances
			if [[ -r "${SUBSUBSUB_DIR}" ]]; then
				ls "${SUBSUBSUB_DIR}" | grep ".cnf" | while read -r FILE ; do
					ABS_FILE="${SUBSUBSUB_DIR}/${FILE}"
					runinstance "${ABS_FILE}"
				done
			else
				echo "Could not read directory ${SUBSUBSUB_DIR}"
			fi
			done
		else
			echo "Could not read directory ${SUBSUB_DIR}"
		fi
	done
done
