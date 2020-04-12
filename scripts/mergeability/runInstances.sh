#bin/sh

PREV_TYPE=""
COUNT=0

# buffer for holding the last k instances
BUFFER=()

# validate input
if [[ $# -ne 3 ]]; then
	echo "Usage: $0 <DIRECTORY> <INSTANCES_CSV> <NUM_TO_EXECUTE>"
	exit 1
fi

MAIN_DIR="${1%/}"
INSTANCES_FILE="$2"
NUM_TO_EXECUTE=$3

# check if input file is readable
if [[ ! -r ${INSTANCES_FILE} ]]; then
	echo "Could not read input file: ${INSTANCES_FILE}"
	exit 1
fi

# run instance
runinstance() {
	echo $1
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

# run instances
while read LINE; do
	ARRAY=(${LINE})
	RATIO=${ARRAY[0]%,*}
	TYPE=${ARRAY[1]%,*}
	FILE=${ARRAY[2]%,*}
	TIME=${ARRAY[3]%,*}
	CNF_FILE="${MAIN_DIR}/ratio${RATIO}/instances/${TYPE}/${FILE}.cnf"

	if [[ "${RATIO}/${TYPE}" != ${PREV_TYPE} ]]; then
		outputbuffer

		# reset type and count
		PREV_TYPE="${RATIO}/${TYPE}"
		COUNT=0
	fi

	# output easy instances
	if [[ $COUNT -lt ${NUM_TO_EXECUTE} ]]; then
		runinstance ${CNF_FILE}
	fi

	# add CNF to buffer
	INDEX=$((COUNT % NUM_TO_EXECUTE))
	BUFFER[${INDEX}]=${CNF_FILE}
	COUNT=$((COUNT + 1))
done < ${INSTANCES_FILE}

outputbuffer
