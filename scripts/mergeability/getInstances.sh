#/bin/sh
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

INSTANCE_TYPES=("medium" "powerlaw" "uniform")

# iterate over all ratios
ls "${MAIN_DIR}" | grep "ratio" | while read -r INNER ; do
	SUB_DIR="${MAIN_DIR}/${INNER}/results"

	# iterate over all instance types
	for INSTANCE_TYPE in "${INSTANCE_TYPES[@]}"; do
		SUBSUB_DIR="${SUB_DIR}/${INSTANCE_TYPE}"
	
		# iterate over all instances
		if [[ -r "${SUBSUB_DIR}" ]]; then
			ls "${SUBSUB_DIR}" | while read -r FILE ; do
				ABS_FILE="${SUBSUB_DIR}/${FILE}"
				if [[ -r ${ABS_FILE} ]]; then
					CPU_TIME=$(cat ${ABS_FILE} | grep 'CPU time')
					CPU_TIME=$(echo "${CPU_TIME#*: }")
					CPU_TIME=$(echo "${CPU_TIME% s}")
					echo "${INNER#ratio}, ${INSTANCE_TYPE}, ${FILE%.log}, ${CPU_TIME}" >> ${TEMP_FILE}
				else
					echo "${INNER#ratio}, ${INSTANCE_TYPE}, ${FILE%.log}" >> ${FAIL_FILE}
					echo "Could not read file ${ABS_FILE}"
				fi
			done
		else
			echo "${INNER}, ${INSTANCE_TYPE}" >> ${FAIL_FILE}
			echo "Could not read directory ${SUBSUB_DIR}"
		fi
	done
done

# sort data
sort -t ',' -k1,1n -k2,2 -k4,4n -k3,3n < ${TEMP_FILE} >> ${OUT_FILE}
rm ${TEMP_FILE}
