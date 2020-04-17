#!/bin/sh

SHARCNET_ACCOUNT_NAME="vganesh"
SHARCNET_TIMEOUT="00:10:00"
SHARCNET_MEMORY="5G"

INTERMEDIATE_FLIPS=10
MAX_FLIPS=100

PREV_TYPE=""
COUNT=0

# buffer for holding the last k instances
BUFFER=()

# validate input
if [[ $# -ne 5 ]]; then
	echo "Usage: $0 <DIRECTORY> <INSTANCES_CSV> <NUM_TO_EXECUTE> <OUT_DIRECTORY> <MERGE_GENERATOR>"
	exit 1
fi

MAIN_DIR="${1%/}"
INSTANCES_FILE="$2"
NUM_TO_EXECUTE=$3
OUT_DIR="${4%/}"
MERGE_GENERATOR=$5

# check if input file is readable
if [[ ! -r ${INSTANCES_FILE} ]]; then
	echo "Could not read input file: ${INSTANCES_FILE}"
	exit 1
fi

# generate merge instances
runinstance() {
	echo "Queuing merge generation for ${1}"

	# create output directory
	OUT_SUB_DIR="${OUT_DIR}/${1}"
	mkdir -p "${OUT_SUB_DIR}"

	# create script to generate merge instances
	JOB_SCRIPT="${OUT_SUB_DIR}/generateMergeInstances.sh"
	echo "#!/bin/bash" > ${JOB_SCRIPT}
	echo "#SBATCH --account=def-${SHARCNET_ACCOUNT_NAME}" >> ${JOB_SCRIPT}
	echo "#SBATCH --time=${SHARCNET_TIMEOUT}" >> ${JOB_SCRIPT}
	echo "#SBATCH --mem=${SHARCNET_MEMORY}" >> ${JOB_SCRIPT}
	echo "#SBATCH --job-name=genMerge" >> ${JOB_SCRIPT}
	echo "#SBATCH --output=${OUT_SUB_DIR}/generateMergeInstances.log" >> ${JOB_SCRIPT}

	# generate merge instances
	OUTPUT_INSTANCE_PREFIX="outputInstance"
	echo "${MERGE_GENERATOR} \"${MAIN_DIR}/${1}.cnf\" \"${OUT_DIR}/${1}/${OUTPUT_INSTANCE_PREFIX}\" \"${INTERMEDIATE_FLIPS}\" \"${MAX_FLIPS}\" 0" >> ${JOB_SCRIPT}
	
	# rename instances
	echo "ls \"${OUT_SUB_DIR}\" | grep \"${OUTPUT_INSTANCE_PREFIX}\" | while read -r CNF_FILE ; do" >> ${JOB_SCRIPT}
	echo "	mv \"${OUT_SUB_DIR}/\${CNF_FILE}\" \"${OUT_SUB_DIR}/\${CNF_FILE#${OUTPUT_INSTANCE_PREFIX}}.cnf\"" >> ${JOB_SCRIPT}
	echo "done" >> ${JOB_SCRIPT}

	# queue job
	sbatch ${JOB_SCRIPT}

	# Wait between queuing jobs
	sleep 2
}

# output hard instances
outputbuffer() {
	if [[ ${COUNT} -gt ${NUM_TO_EXECUTE} ]]; then
		NUM_TO_OUTPUT=$((COUNT - NUM_TO_EXECUTE))
		if [[ ${NUM_TO_OUTPUT} -gt ${NUM_TO_EXECUTE} ]]; then
			NUM_TO_OUTPUT=${NUM_TO_EXECUTE}
		fi
		START_INDEX=$(((COUNT - NUM_TO_OUTPUT) % NUM_TO_EXECUTE))
		END_INDEX=$((START_INDEX + NUM_TO_OUTPUT))

		while [[ ${START_INDEX} -lt ${END_INDEX} ]]; do
			INDEX=$((START_INDEX % NUM_TO_EXECUTE))
			runinstance "${BUFFER[${INDEX}]}"
			START_INDEX=$((START_INDEX + 1))
		done
	fi
}

# generate merge instances
while read LINE; do
	ARRAY=(${LINE})
	RATIO=${ARRAY[0]%,*}
	TYPE=${ARRAY[1]%,*}
	FILE=${ARRAY[2]%,*}
	TIME=${ARRAY[3]%,*}
	BASE_FILE_NAME="ratio${RATIO}/instances/${TYPE}/${FILE}"

	if [[ "${RATIO}/${TYPE}" != ${PREV_TYPE} ]]; then
		outputbuffer

		# reset type and count
		PREV_TYPE="${RATIO}/${TYPE}"
		COUNT=0
	fi

	# output easy instances
	if [[ $COUNT -lt ${NUM_TO_EXECUTE} ]]; then
		runinstance ${BASE_FILE_NAME}
	fi

	# add CNF to buffer
	INDEX=$((COUNT % NUM_TO_EXECUTE))
	BUFFER[${INDEX}]=${BASE_FILE_NAME}
	COUNT=$((COUNT + 1))
done < ${INSTANCES_FILE}

outputbuffer
