#!/bin/sh

SHARCNET_ACCOUNT_NAME="vganesh"
SHARCNET_TIMEOUT="00:00:5000"
SHARCNET_MEMORY="5G"



if [[ $# -ne 3 ]]; then
	echo "Usage: $0 <DIRECTORY> <MERGE_COMPILED> <COMMUNITY_FILE>"
	exit 1
fi

MAIN_DIR="${1%/}"
MERGE_COMPILED="$2"


runinstance() {
	LINE=($(head -n 1 ${1}))
	NUMVARS=${LINE[2]}
	COMM_TEMP="${INSTANCE_NAME}_comm"
	COUNT=1

	while [ $COUNT -lt $NUMVARS ]
	do
		echo "$COUNT 1 \n" > $COMM_TEMP
		COUNT=$(($COUNT + 1))
	done
	
	INSTANCE_NAME="${1%.cnf}"
	echo "Queuing mergeability-calculating for ${1}"

	JOB_SCRIPT="${INSTANCE_NAME}_merge.sh"
	echo "#!/bin/bash" > ${JOB_SCRIPT}
	echo "#SBATCH --account=def-${SHARCNET_ACCOUNT_NAME}" >> ${JOB_SCRIPT}
	echo "#SBATCH --time=${SHARCNET_TIMEOUT}" >> ${JOB_SCRIPT}
	echo "#SBATCH --mem=${SHARCNET_MEMORY}" >> ${JOB_SCRIPT}
	echo "#SBATCH --job-name=mergeCalc" >> ${JOB_SCRIPT}
	echo "#SBATCH --output=${INSTANCE_NAME}_mergejob.log" >> ${JOB_SCRIPT}

	echo "${MERGE_COMPILED} ${1} ${COMM_TEMP} ${INSTANCE_NAME}_merge.log" >> ${JOB_SCRIPT}

	sbatch ${JOB_SCRIPT}

	sleep 2
}
		




find ${MAIN_DIR} -name '*.cnf' | while read -r CNF_FILE ; do
	runinstance "${CNF_FILE}"
done
