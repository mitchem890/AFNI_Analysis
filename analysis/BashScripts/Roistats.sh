#!/usr/bin/env bash

# This Script is a simplified script of the roistats_*.sh that are to be used with the python  Afni_analysis script


while getopts :i:n:w:a:r:b:f: option
do
  case "${option}"
  in
    i) input_file=${OPTARG};; #The input stats file that we will be using to get all the data out. Should include directory path
    n) name=${OPTARG};;
    w) work_dir=${OPTARG};; #Where are all the inputs and outputs
    a) atlas=${OPTARG};; #The atlas that we will be using to parcellate should include directory path
    r) extension=${OPTARG};;
    b) subbrick=${OPTARG};;
    f) outfile=${OPTARG};;
  esac
done

if [ ! -f "${input_file}" ]; then
    echo "${input_file} does not exist exiting roistats"
    exit
fi


TFILE=$(mktemp)

# Get the index of the subbricks
3dinfo -verb ${input_file} | grep "${subbrick}" | grep "'${name}#" > $TFILE
idx=$(echo $(awk '{print $4}' $TFILE))
echo "${idx[@]//#}" > "${work_dir}/idx_${name}_${subbrick}.1D"


atlas_file=$(basename ${atlas})
# roistats
3dROIstats -overwrite -mask "${atlas}${extension}" "${input_file}[1dcat ${work_dir}/idx_${name}_${subbrick}.1D]"  > "${work_dir}/${outfile}"

rm $TFILE
