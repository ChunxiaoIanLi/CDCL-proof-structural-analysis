#!/bin/bash
# ./run_test.sh 20 352 ../main ../../../../glucose-3.0D/core/glucose ../../../../drat-trim/drat-trim

if [[ $# -ne 6 ]]; then
    echo "Usage: $0 <NUM_SHA_ROUNDS> <NUM_TO_RESTRICT> <CRYPTO_EXEC> <RESTRICT_EXEC> <GLUCOSE_EXEC> <DRAT_EXEC>"
    exit 1
fi

NUM_SHA_ROUNDS=$1
NUM_TO_RESTRICT=$2
CRYPTO_EXEC=$3
RESTRICT_EXEC=$4
GLUCOSE_EXEC=$5
DRAT_EXEC=$6

GENERATE_PROOF="false"

TMP_DIRECTORY="./generated/"
BASE_NAME="SHA1_${NUM_SHA_ROUNDS}_${NUM_TO_RESTRICT}"

GENERATED_CNF="${BASE_NAME}.cnf"
RESTRICTED_CNF="${BASE_NAME}_restricted.cnf"
GLUCOSE_LOG="${BASE_NAME}_glucose.log"
GENERATED_DRAT="${GENERATED_CNF}.drat"
GENERATED_CORE="${GENERATED_DRAT}.core"

GENERATED_CNF="${TMP_DIRECTORY}${GENERATED_CNF}"
RESTRICTED_CNF="${TMP_DIRECTORY}${RESTRICTED_CNF}"
GLUCOSE_LOG="${TMP_DIRECTORY}${GLUCOSE_LOG}"
GENERATED_DRAT="${TMP_DIRECTORY}${GENERATED_DRAT}"
GENERATED_CORE="${TMP_DIRECTORY}${GENERATED_CORE}"

echo
echo "----------------------------------"
echo "CRYPTO_EXEC:     $CRYPTO_EXEC"
echo "RESTRICT_EXEC:   $RESTRICT_EXEC"
echo "GLUCOSE_EXEC:    $GLUCOSE_EXEC"
echo "DRAT_EXEC:       $DRAT_EXEC"
echo "----------------------------------"
echo "NUM_SHA_ROUNDS:  $NUM_SHA_ROUNDS"
echo "NUM_TO_RESTRICT: $NUM_TO_RESTRICT"
echo "GENERATED_CNF:   $GENERATED_CNF"
echo "RESTRICTED_CNF:  $RESTRICTED_CNF"
echo "GLUCOSE_LOG:     $GLUCOSE_LOG"
echo "GENERATED_DRAT:  $GENERATED_DRAT"
echo "----------------------------------"
echo

mkdir -p $TMP_DIRECTORY

# Generate CNF from a randomly generated SHA-1 instance
echo "Generating CNF from SHA-1 instance..."
$CRYPTO_EXEC -A counter_chain -r $NUM_SHA_ROUNDS --random_target --print_target |
$CRYPTO_EXEC -A counter_chain -r $NUM_SHA_ROUNDS > $GENERATED_CNF

# Flip n bits in the generated CNF
echo "Restricting CNF..."
$RESTRICT_EXEC "$NUM_TO_RESTRICT" "$GENERATED_CNF" "$RESTRICTED_CNF"

# Run glucose on instance
if [[ $GENERATE_PROOF == "true" ]]; then
    echo "Solving instance and generating DRAT proof with glucose..."
    $GLUCOSE_EXEC -certified -certified-output="$GENERATED_DRAT" $RESTRICTED_CNF > $GLUCOSE_LOG

    # Generate DRAT proof
    echo "Generating core DRAT proof..."
    $DRAT_EXEC "$RESTRICTED_CNF" "$GENERATED_DRAT" -c $GENERATED_CORE
else
    echo "Solving instance with glucose..."
    $GLUCOSE_EXEC $RESTRICTED_CNF > $GLUCOSE_LOG
fi
