#!/bin/bash
# This script generates a core proof for a drat proof

if [[ $# -ne 6 ]]; then
    echo "Usage: $0 <BEGIN_ROUNDS> <END_ROUNDS> <BEGIN_RESTRICTIONS> <END_RESTRICTIONS> <OUT_DIRECTORY> <DRAT_EXEC>"
    exit 1
fi

BEGIN_ROUNDS=$1
END_ROUNDS=$2
BEGIN_RESTRICTIONS=$3
END_RESTRICTIONS=$4
OUT_DIRECTORY=$5
DRAT_EXEC=$6

SHARCNET_ACCOUNT_NAME="vganesh"
SHARCNET_TIMEOUT="24:00:00"
SHARCNET_MEMORY="2G"

if [[ $END_ROUNDS < $BEGIN_ROUNDS ]]; then
    echo "Cannot begin rounds after the end"
    exit 1
fi

if [[ $END_RESTRICTIONS < $BEGIN_RESTRICTIONS ]]; then
    echo "Cannot begin restrictions after the end"
    exit 1
fi

mkdir -p $OUT_DIRECTORY

for ((i = $BEGIN_ROUNDS; i <= $END_ROUNDS; i++)); do
    OUT_SUBDIRECTORY="${OUT_DIRECTORY}/${i}_rounds"
    mkdir -p $OUT_SUBDIRECTORY

    for ((j = $BEGIN_RESTRICTIONS; j <= $END_RESTRICTIONS; j++)); do
        OUT_SUBSUBDIRECTORY="${OUT_SUBDIRECTORY}/${j}_restrictions"
        mkdir -p $OUT_SUBSUBDIRECTORY

        BASE_NAME="${i}_${j}_SHA1"
        RESTRICTED_CNF="${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_restricted.cnf"
        DRAT_PROOF="${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_proof.drat"
        CORE_PROOF="${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_core.drat"

        # Generate job file
        echo "Generating job script"
        JOB_SCRIPT="${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_drat_trim.sh"
        echo "#!/bin/bash" > $JOB_SCRIPT
        echo "#SBATCH --account=def-${SHARCNET_ACCOUNT_NAME}" >> $JOB_SCRIPT
        echo "#SBATCH --time=${SHARCNET_TIMEOUT}" >> $JOB_SCRIPT
        echo "#SBATCH --mem=${SHARCNET_MEMORY}" >> $JOB_SCRIPT
        echo "#SBATCH --job-name=${BASE_NAME}_solve" >> $JOB_SCRIPT
        echo "#SBATCH --output=${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_output.txt" >> $JOB_SCRIPT

        echo "${DRAT_EXEC} ${RESTRICTED_CNF} ${DRAT_PROOF} -c ${CORE_PROOF}" >> $JOB_SCRIPT

        # Queue job
        sbatch $JOB_SCRIPT

        # Wait between queuing jobs
        sleep 2
    done
done