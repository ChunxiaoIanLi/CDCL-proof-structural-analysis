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
# @param $10: mergeability score
# @param $11: normalized mergeability score (mergeability score / number of clauses^2)
# @param $12: normalized mergeability score (mergeability score / resolvability)
# @param $13: total clause width
# @param $14: total post-resolution clause width
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
	local mrg=-1
	local _m2=-1
	local _m3=-1
	local _ms=-1
	local ms2=-1
	local ms3=-1
	if [[ -f "${ins}.rvm" ]]; then
		local tmp=(`head -n 1 ${ins}.rvm`)
		res=${tmp[0]}
		mrg=${tmp[1]}
		_ms=${tmp[2]}
		tmp=$(changeExpNotation ${_ms})
		_m2=$(bc -l <<< "${mrg} / (${_m_} * ${_m_})")
		ms2=$(bc -l <<< "${tmp} / (${_m_} * ${_m_})")
		if [[ ${res} != "0" ]]; then
			_m3=$(bc -l <<< "${mrg} / ${res}");
			ms3=$(bc -l <<< "${tmp} / ${res}");
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

	local params="${_n_} ${_m_} ${_t_} ${cvr} ${res} ${mrg} ${_m2} ${_m3} ${_ms} ${ms2} ${ms3} ${cw1} ${cw2} ${sat}"

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
		local delta_n_=-1; if [[ ${2}  != "0" ]]; then delta_n_=$(bc -l <<< "${_n_}/${2}"); fi
		local delta_m_=-1; if [[ ${3}  != "0" ]]; then delta_m_=$(bc -l <<< "${_m_}/${3}"); fi
		local delta_t_=-1; if [[ ${4}  != "0" ]]; then delta_t_=$(bc -l <<< "${_t_}/${4}"); fi
		local deltacvr=-1; if [[ ${5}  != "0" ]]; then deltacvr=$(bc -l <<< "${cvr}/${5}"); fi
		local deltares=-1; if [[ ${6}  != "0" ]]; then deltares=$(bc -l <<< "${res}/${6}"); fi
		local deltamrg=-1; if [[ ${7}  != "0" ]]; then deltamrg=$(bc -l <<< "${mrg}/${7}"); fi
		local delta_m2=-1; if [[ ${8}  != "0" ]]; then delta_m2=$(bc -l <<< "${_m2}/${8}"); fi
		local delta_m3=-1; if [[ ${9}  != "0" ]]; then delta_m3=$(bc -l <<< "${_m3}/${9}"); fi
		local delta_ms=-1; if [[ ${10} != "0" ]]; then delta_ms=$(bc -l <<< "$(changeExpNotation ${_ms})/$(changeExpNotation ${10})"); fi
		local deltams2=-1; if [[ ${11} != "0" ]]; then deltams2=$(bc -l <<< "$(changeExpNotation ${ms2})/$(changeExpNotation ${11})"); fi
		local deltams3=-1; if [[ ${12} != "0" ]]; then deltams3=$(bc -l <<< "$(changeExpNotation ${ms3})/$(changeExpNotation ${12})"); fi
		local deltacw1=-1; if [[ ${13} != "0" ]]; then deltacw1=$(bc -l <<< "${cw1}/${13}"); fi
		local deltacw2=-1; if [[ ${14} != "0" ]]; then deltacw2=$(bc -l <<< "${cw2}/${14}"); fi

		# Output params for pre-processed instances
		echo "${ins},${_n_},${delta_n_},${_m_},${delta_m_},${_t_},${delta_t_},${cvr},${deltacvr},${res},${deltares},${mrg},${deltamrg},${_m2},${delta_m2},${_m3},${delta_m3},${_ms},${delta_ms},${ms2},${deltams2},${ms3},${deltams3},${cw1},${deltacw1},${cw2},${deltacw2},${sat}"
	fi
}

# Output CSV header
headers="vars,clauses,solving time,cvr,resolvability,total merges,total merges/m^2,total merges/resolvability,mergeability score,mergeability score/m^2,mergeability score/resolvability,average pre-resolution clause width,average post-resolution clause width,satisfiability"
echo "instance,${headers}," > "${output_base}"
headers="${headers//,/,%change,},"
echo "instance,${headers}" > "${output_maplesat}"
echo "instance,${headers}" > "${output_glucose}"
echo "instance,${headers}" > "${output_summary}"

# Output data for each instance
for i in $(getBaseInstances "${directory}")
do
    # Print beta:
    #cat /scratch/ianli/parameters_of_industiral/verification/fitted_powerlaw/c_bounded_model_checker/$i.dv_fitted.log | head -n 1 | cut -d' ' -f2
    #cat /scratch/ianli/parameters_of_industiral/verification/fitted_powerlaw/c_bounded_model_checker/$i\_preprocess.dv_fitted.log | head -n 1 | cut -d' ' -f2

    # Data for original
    fetchData "${i}"
done
