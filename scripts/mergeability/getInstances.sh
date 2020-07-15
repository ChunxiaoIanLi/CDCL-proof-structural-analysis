#!/bin/sh
TEMP_FILE="instances.tmp"
FAIL_FILE="error.csv"

# validate input
if [[ $# -ne 2 ]]; then
	echo "Usage: $0 <DIRECTORY> <OUTPUT_FILE>"
	exit 1
fi

MAIN_DIR="${1%/}"
OUT_FILE="$2"

shopt -s extglob

# reset temp file
if [[ -e ${TEMP_FILE} ]]; then
	rm ${TEMP_FILE}
fi

# reset error file
if [[ -e ${FAIL_FILE} ]]; then
	rm ${FAIL_FILE}
fi

echo "ratio, instance type, instance id" > ${FAIL_FILE}

# reset output file
if [[ -e ${OUT_FILE} ]]; then
	rm ${OUT_FILE}
fi

# echo "ratio, instance type, instance id, cpu time"

# iterate over all ratios

BASE_DIR="${MAIN_DIR%/ratio*}"

find ${MAIN_DIR} -name '*.log' | while read -r ABS_FILE ; do
	REL_FILE="${ABS_FILE#*/ratio}"
	RATIO=${REL_FILE%%/*}
	REL_FILE="${REL_FILE#${RATIO}/results/}"
	INSTANCE_TYPE=${REL_FILE%%/*}
	REL_FILE="${REL_FILE#${INSTANCE_TYPE}/}"
	INSTANCE_ID="${REL_FILE%.log}"
	
	if [[ -r ${ABS_FILE} ]]; then
		CPU_TIME=$(cat ${ABS_FILE} | grep 'CPU time')
		CPU_TIME="${CPU_TIME#*: }"
		CPU_TIME="${CPU_TIME% s}"
		IS_SAT=$(cat ${ABS_FILE} | grep 'SATISFIABLE')

		echo "${RATIO}, ${INSTANCE_TYPE}, ${INSTANCE_ID}, ${CPU_TIME}, ${IS_SAT}" >> ${TEMP_FILE}
	else
		echo "${RATIO}, ${INSTANCE_TYPE}, ${INSTANCE_ID}" >> ${FAIL_FILE}
		echo "Could not read file ${ABS_FILE}"
	fi
done

# sort data
sort -t ',' -k1,1 -k2,2 -k4,4n -k3,3n < ${TEMP_FILE} >> ${OUT_FILE}
rm ${TEMP_FILE}
