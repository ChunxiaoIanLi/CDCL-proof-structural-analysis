#!/bin/bash
# This script queues a SHARCNET job for every round-restriction combination

if [[ $# -ne 8 ]]; then
    echo "Usage: $0 <BEGIN_ROUNDS> <END_ROUNDS> <BEGIN_RESTRICTIONS> <END_RESTRICTIONS> <OUT_DIRECTORY> <CRYPTO_EXEC> <RESTRICT_EXEC> <GLUCOSE_EXEC>"
    exit 1
fi

BEGIN_ROUNDS=$1
END_ROUNDS=$2
BEGIN_RESTRICTIONS=$3
END_RESTRICTIONS=$4
OUT_DIRECTORY=$5
CRYPTO_EXEC=$6
RESTRICT_EXEC=$7
GLUCOSE_EXEC=$8

GENERATE_PROOF="true"

SHARCNET_ACCOUNT_NAME="vganesh"
SHARCNET_TIMEOUT="2:00:00"
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
        GENERATED_CNF="${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_generated.cnf"
        RESTRICTED_CNF="${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_restricted.cnf"

        # Generate CNF from a randomly generated SHA-1 instance
        echo "Generating CNF from SHA-1 instance with ${i} rounds and ${j} restrictions..."
        $CRYPTO_EXEC -A counter_chain -r $i --random_target --print_target |
        $CRYPTO_EXEC -A counter_chain -r $i > $GENERATED_CNF

        # Flip n random bits in the generated CNF
        $RESTRICT_EXEC "$j" "$GENERATED_CNF" "$RESTRICTED_CNF"

        # Generate job file
        echo "Generating job script"
        JOB_SCRIPT="${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_run-glucose.sh"
        echo "#!/bin/bash" > $JOB_SCRIPT
        echo "#SBATCH --account=def-${SHARCNET_ACCOUNT_NAME}" >> $JOB_SCRIPT
        echo "#SBATCH --time=${SHARCNET_TIMEOUT}" >> $JOB_SCRIPT
        echo "#SBATCH --mem=${SHARCNET_MEMORY}" >> $JOB_SCRIPT
        echo "#SBATCH --job-name=${BASE_NAME}_solve" >> $JOB_SCRIPT
        echo "#SBATCH --output=${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_glucose.log" >> $JOB_SCRIPT

        PROOF_FILE="${OUT_SUBSUBDIRECTORY}/${BASE_NAME}_proof.drat"

        echo "echo \"CPU information:\"" >> $JOB_SCRIPT
        echo "echo \$(lscpu)" >> $JOB_SCRIPT
        echo "echo" >> $JOB_SCRIPT
        echo "echo \"RAM information:\"" >> $JOB_SCRIPT
        echo "echo \$(free -m)" >> $JOB_SCRIPT

        echo "start=\$((\$(date +%s%N)/1000000))" >> $JOB_SCRIPT
        if [[ $GENERATE_PROOF == "true" ]]; then
            echo "${GLUCOSE_EXEC} -certified -certified-output=\"${PROOF_FILE}\" ${RESTRICTED_CNF}" >> $JOB_SCRIPT
        else
            echo "${GLUCOSE_EXEC} ${RESTRICTED_CNF}" >> $JOB_SCRIPT
        fi
        echo "end=\$((\$(date +%s%N)/1000000))" >> $JOB_SCRIPT

        echo "diff=\$((\$end-\$start))" >> $JOB_SCRIPT
        echo "echo \"Glucose executed in:\" \$diff \"milliseconds\"" >> $JOB_SCRIPT

        # Queue job
        sbatch $JOB_SCRIPT

        # Wait between queuing jobs
        sleep 2
    done
done