#!/bin/bash

# Validate input arguments
# @param $1: input directory
# @param $2: base name for the output CSV. There are 4 outputs.
# @output <BASE_NAME>.CSV - only the outputs for the base instances
# @output <BASE_NAME>_maplesat_preprocess.csv - only the outputs for the instances preprocessed by maplesat
# @output <BASE_NAME>_glucose_preprocess.csv - only the outputs for the instances preprocessed by glucose
# @output <BASE_NAME>_summary.csv
if [[ $# -ne 2 ]]; then
	echo "Usage: $0 <DIRECTORY> <OUTPUT_CSV_BASE_NAME>"
	exit 1
fi

directory="${1%/}"
output_base="${2}.csv"
output_maplesat="${2}_maplesat_preprocess.csv"
output_glucose="${2}_glucose_preprocess.csv"
output_summary="${2}_summary.csv"

# Get the list of all base (non-preprocessed) instances in the directory
getBaseInstances() {
	for instance in $(find $directory -name "*.cnf" | grep -v "preprocess"); do
		echo "${instance%.cnf}"
	done
}

# Get a string representing an instance's satisfiability
# @param $1: instance name
getSat() {
	local ins=$1	
	if grep -q "UNSATISFIABLE" "${ins}.log"; then
		echo "UNSATISFIABLE"
	elif grep -q "SATISFIABLE" "${ins}.log"; then
		echo "SATISFIABLE"
	else
		echo "INDETERMINATE"
	fi
}

# Convert from exponential notation to a form understandable by bc
# @param $1: value
changeExpNotation() {
	sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<< "${1}"
}

# Get a CSV string of an instance's parameters
# @param $1: instance name
# [OPTIONAL] parameters in base instance
# @param $2: number of variables
# @param $3: number of clauses
# @param $4: solving time
# @param $5: cvr
# @param $6: resolvability
# @param $7: total merges
# @param $8: normalized total merges (total merges / number of clauses^2)
# @param $9: normalized total merges (total merges / resolvability)
# @param $10: mergeability score 1 (num_merge_literals / (width_1 + width_2 - 2))
# @param $11: normalized mergeability score 1 (mergeability score / number of clauses^2)
# @param $12: normalized mergeability score 1 (mergeability score / resolvability)
# @param $13: mergeability score 2 (num_merge_literals / (width_1 + width_2 - num_merge_literals - 2))
# @param $14: normalized mergeability score 2 (mergeability score / number of clauses^2)
# @param $15: normalized mergeability score 2 (mergeability score / resolvability)
# @param $16: total clause width
# @param $17: total post-resolution clause width
fetchData() {
	local num=$#
	local ins=$1

	# Read parameters
	local _n_=-1
	local _m_=-1
	local cvr=-1
	if [[ -f "${ins}.cvr" ]]; then
		local tmp=(`head -n 1 ${ins}.cvr`)
		_m_=${tmp[0]}
		_n_=${tmp[1]}
		cvr=${tmp[2]}
	fi

	local res=-1
	local mrg1=-1
	local mrg2=-1
	local mrg3=-1
	local ms11=-1
	local ms12=-1
	local ms13=-1
	local ms21=-1
	local ms22=-1
	local ms23=-1
	if [[ -f "${ins}.rvm" ]]; then
		local tmp=(`head -n 1 ${ins}.rvm`)
		res=${tmp[0]}
		mrg1=${tmp[1]}
		ms11=${tmp[2]}
		ms21=${tmp[3]}
		local tmp1=$(changeExpNotation ${ms11})
		local tmp2=$(changeExpNotation ${ms21})
		mrg2=$(bc -l <<< "${mrg1} / (${_m_} * ${_m_})")
		ms12=$(bc -l <<< "${tmp1} / (${_m_} * ${_m_})")
		ms22=$(bc -l <<< "${tmp2} / (${_m_} * ${_m_})")
		if [[ ${res} != "0" ]]; then
			mrg3=$(bc -l <<< "${mrg1} / ${res}");
			ms13=$(bc -l <<< "${tmp1} / ${res}");
			ms23=$(bc -l <<< "${tmp2} / ${res}");
		fi
	fi

	local _t_=-1
	local sat="FILE_DOES_NOT_EXIST"
	if [[ -f "${ins}.log" ]]; then
		_t_=$(grep -m 1 "CPU" ${ins}.log | awk '{print $4}')
		sat=$(getSat "${ins}")
	fi

	local cw1=-1
	local cw2=-1
	if [[ -f "${ins}.tcw" ]]; then
		local tmp=(`head -n 1 ${ins}.tcw`)
		cw1=$(bc -l <<< "${tmp[0]}/${_m_}")
		cw2=$(bc -l <<< "${tmp[1]}/${res}")
	fi

	local params="${_n_} ${_m_} ${_t_} ${cvr} ${res} ${mrg1} ${mrg2} ${mrg3} ${ms11} ${ms12} ${ms13} ${ms21} ${ms22} ${ms23} ${cw1} ${cw2} ${sat}"

	if [[ $num -eq 1 ]]; then
		# Output params for base instance
		echo "${ins},${params// /,}" >> "${output_base}"
		echo "${ins},${params// /,,}" >> "${output_summary}"

		# Output params for pre-processed instances
		maplesatStr=$(fetchData "${ins}_maplesat_preprocess" ${params})
		glucoseStr=$(fetchData "${ins}_glucose_preprocess"  ${params})
		echo "${maplesatStr}" >> "${output_maplesat}"
		echo "${maplesatStr}" >> "${output_summary}"
		echo "${glucoseStr}" >> "${output_glucose}"
		echo "${glucoseStr}" >> "${output_summary}"
	else
		# Calculate percentage change
		local delta_n_=-1; if [[ ${2} != "0" ]]; then delta_n_=$(bc -l <<< "${_n_}/${2}"); fi
		local delta_m_=-1; if [[ ${3} != "0" ]]; then delta_m_=$(bc -l <<< "${_m_}/${3}"); fi
		local delta_t_=-1; if [[ ${4} != "0" ]]; then delta_t_=$(bc -l <<< "${_t_}/${4}"); fi
		local deltacvr=-1; if [[ ${5} != "0" ]]; then deltacvr=$(bc -l <<< "${cvr}/${5}"); fi
		local deltares=-1; if [[ ${6} != "0" ]]; then deltares=$(bc -l <<< "${res}/${6}"); fi
		local deltamrg1=-1; if [[ ${7} != "0" ]]; then deltamrg1=$(bc -l <<< "${mrg1}/${7}"); fi
		local deltamrg2=-1; if [[ ${8} != "0" ]]; then deltamrg2=$(bc -l <<< "${mrg2}/${8}"); fi
		local deltamrg3=-1; if [[ ${9} != "0" ]]; then deltamrg3=$(bc -l <<< "${mrg3}/${9}"); fi
		local deltams11=-1; if [[ ${10} != "0" ]]; then deltams11=$(bc -l <<< "$(changeExpNotation ${ms11})/$(changeExpNotation ${10})"); fi
		local deltams12=-1; if [[ ${11} != "0" ]]; then deltams12=$(bc -l <<< "$(changeExpNotation ${ms12})/$(changeExpNotation ${11})"); fi
		local deltams13=-1; if [[ ${12} != "0" ]]; then deltams13=$(bc -l <<< "$(changeExpNotation ${ms13})/$(changeExpNotation ${12})"); fi
		local deltams21=-1; if [[ ${13} != "0" ]]; then deltams21=$(bc -l <<< "$(changeExpNotation ${ms21})/$(changeExpNotation ${13})"); fi
		local deltams22=-1; if [[ ${14} != "0" ]]; then deltams22=$(bc -l <<< "$(changeExpNotation ${ms22})/$(changeExpNotation ${14})"); fi
		local deltams23=-1; if [[ ${15} != "0" ]]; then deltams23=$(bc -l <<< "$(changeExpNotation ${ms23})/$(changeExpNotation ${15})"); fi
		local deltacw1=-1; if [[ ${16} != "0" ]]; then deltacw1=$(bc -l <<< "${cw1}/${16}"); fi
		local deltacw2=-1; if [[ ${17} != "0" ]]; then deltacw2=$(bc -l <<< "${cw2}/${17}"); fi

		# Output params for pre-processed instances
		echo "${ins},${_n_},${delta_n_},${_m_},${delta_m_},${_t_},${delta_t_},${cvr},${deltacvr},${res},${deltares},${mrg1},${deltamrg1},${mrg2},${deltamrg2},${mrg3},${deltamrg3},${ms11},${deltams11},${ms12},${deltams12},${ms13},${deltams13},${ms21},${deltams21},${ms22},${deltams22},${ms23},${deltams23},${cw1},${deltacw1},${cw2},${deltacw2},${sat}"
	fi
}

# Output CSV header
headers="vars,clauses,solving time,cvr,resolvability,total merges,total merges/m^2,total merges/resolvability,mergeability_score_1,mergeability_score_1/m^2,mergeability_score_1/resolvability,mergeability_score_2,mergeability_score_2/m^2,mergeability_score_2/resolvability,average pre-resolution clause width,average post-resolution clause width,satisfiability"
echo "instance,${headers}," > "${output_base}"
headers="${headers//,/,%change,},"
echo "instance,${headers}" > "${output_maplesat}"
echo "instance,${headers}" > "${output_glucose}"
echo "instance,${headers}" > "${output_summary}"

# Output data for each instance
for i in $(getBaseInstances "${directory}")
do
    # Data for original
    fetchData "${i}"
done
