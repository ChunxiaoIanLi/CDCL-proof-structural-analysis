#bin/sh

PREV_TYPE=""
COUNT=0

# buffer for holding the last k instances
BUFFER=()

# validate input
if [[ $# -ne 5 ]]; then
	echo "Usage: $0 <DIRECTORY> <INSTANCES_CSV> <NUM_TO_EXECUTE> <INTERMEDIATE_FLIPS> <MAX_FLIPS>"
	exit 1
fi

MAIN_DIR="${1%/}"
INSTANCES_FILE="$2"
NUM_TO_EXECUTE=$3
INTERMEDIATE_FLIPS=$4
MAX_FLIPS=$5

# check if input file is readable
if [[ ! -r ${INSTANCES_FILE} ]]; then
	echo "Could not read input file: ${INSTANCES_FILE}"
	exit 1
fi

# run instance
runinstance() {
	FILENAME=$1 | rev | cut -d "/" -f 1 | rev
	../../../proof_graph_analyzer/merge_generator $1 "./${FILENAME}.out" INTERMEDIATE_FLIPS MAX_FLIPS $2


	echo "running merge_generator for $1"
}

# output hard instances
outputbuffer() {
	if [[ ${COUNT} -gt ${NUM_TO_EXECUTE} ]]; then
		NUM_TO_OUTPUT=$((COUNT - NUM_TO_EXECUTE))
		if [[ ${NUM_TO_OUTPUT} -gt ${NUM_TO_EXECUTE} ]]; then
			NUM_TO_OUTPUT=${NUM_TO_EXECUTE}
		fi
		START_INDEX=${INDEX}
		END_INDEX=$((START_INDEX + NUM_TO_OUTPUT))

		while [[ ${START_INDEX} -lt ${END_INDEX} ]]; do
			INDEX=$((START_INDEX % NUM_TO_EXECUTE))
			runinstance "${BUFFER[${INDEX}]}" 1
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
		runinstance ${CNF_FILE} 0
	fi

	COUNT=$((COUNT + 1))

	# add CNF to buffer
	INDEX=$((COUNT % NUM_TO_EXECUTE))
	BUFFER[${INDEX}]=${CNF_FILE}
done < ${INSTANCES_FILE}

outputbuffer
