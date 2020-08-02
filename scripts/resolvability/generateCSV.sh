#!/bin/bash

# Validate input arguments
if [[ $# -ne 1 ]]; then
	echo "Usage: $0 <DIRECTORY>"
	exit 1
fi

directory="${1%/}"

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

# Get a CSV string of an instance's parameters
# @param $1: instance name
# [OPTIONAL] parameters in base instance
# @param $2: number of variables
# @param $3: number of clauses
# @param $4: cvr
# @param $5: resolvability
# @param $6: mergeability
# @param $7: solving time
# @param $8: normalized mergeability (mergeability / number of clauses^2)
fetchData() {
	local num=$#
	local ins=$1
	local _n_=$(grep -m 1 "Number of variables:" ${ins}.log | awk '{print $5}')
	local _m_=$(grep -m 1 "Number of clauses:" ${ins}.log | awk '{print $5}')
	local cvr=$(head -n 1 ${ins}.cvr)
	local tmp=(`head -n 1 ${ins}.rvm`)
	local res=${tmp[0]}
	local mrg=${tmp[1]}
	local _t_=$(grep -m 1 "CPU" ${ins}.log | awk '{print $4}')
	local _m2=$(bc -l <<< "${mrg} / (${_m_} * ${_m_})")
	local sat=$(getSat "${ins}")
	local params="${_n_} ${_m_} ${cvr} ${res} ${mrg} ${_t_} ${_m2} ${sat}"

	if [[ $num -eq 1 ]]; then
		# Output params for base instance
		echo "${ins},${_n_},,${_m_},,${cvr},,${res},,${mrg},,${_t_},,${_m2},,${sat},"

		# Output params for pre-processed instances
		fetchData "${ins}_maplesat_preprocess" ${params}
		fetchData "${ins}_glucose_preprocess" ${params}
	else
		# Calculate percentage change
		local delta_n_=-1; if [[ ${2} != "0" ]]; then delta_n_=$(bc -l <<< "${_n_}/${2}"); fi
		local delta_m_=-1; if [[ ${3} != "0" ]]; then delta_m_=$(bc -l <<< "${_m_}/${3}"); fi
		local deltacvr=-1; if [[ ${4} != "0" ]]; then deltacvr=$(bc -l <<< "${cvr}/${4}"); fi
		local deltares=-1; if [[ ${5} != "0" ]]; then deltares=$(bc -l <<< "${res}/${5}"); fi
		local deltamrg=-1; if [[ ${6} != "0" ]]; then deltamrg=$(bc -l <<< "${mrg}/${6}"); fi
		local delta_t_=-1; if [[ ${7} != "0" ]]; then delta_t_=$(bc -l <<< "${_t_}/${7}"); fi
		local delta_m2=-1; if [[ ${8} != "0" ]]; then delta_m2=$(bc -l <<< "${_m2}/${8}"); fi

		# Output params for pre-processed instances
		echo "${ins},${_n_},${delta_n_},${_m_},${delta_m_},${cvr},${deltacvr},${res},${deltares},${mrg},${deltamrg},${_t_},${delta_t_},${_m2},${delta_m2},${sat},"
	fi
}

# Output CSV header
echo "instance, vars, %change, clauses, %change, cvr, %change, resolvability, %change, mergeability, %change, solving time, %change, mergeability/m^2, %change, satisfiability"

# Output data for each instance
for i in $(getBaseInstances "${directory}")
do
    # Print beta:
    #cat /scratch/ianli/parameters_of_industiral/verification/fitted_powerlaw/c_bounded_model_checker/$i.dv_fitted.log | head -n 1 | cut -d' ' -f2
    #cat /scratch/ianli/parameters_of_industiral/verification/fitted_powerlaw/c_bounded_model_checker/$i\_preprocess.dv_fitted.log | head -n 1 | cut -d' ' -f2

    # Data for original
    fetchData "${i}"
done
