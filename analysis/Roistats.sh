#!/usr/bin/env bash

# This Script is a simplified script of the roistats_*.sh that are to be used with the python  Afni_analysis script


while getopts i:n:d:w:a:e:s:r:o option
do
case "${option}"
in
i) input_file=${OPTARG};; #The input stats file that we will be using to get all the data out. Should include directory path
n) name=${OPTARG};; 
d) design=${OPTARG};;
w) work_dir=${OPTARG};; #Where are all the inputs and outputs
a) atlas=${OPTARG};; #The atlas that we will be using to parcellate should include directory path
e) session=${OPTARG};;
s) subject=${OPTARG};;
o) postfix=${OPTARG};; 
r) extension=${OPTARG};;
esac
done

echo 
echo "The Subject number is ${subject}"
TFILE=$(mktemp)

echo "This is my extention ${extension}"

# Beta coeffs
3dinfo -verb ${input_file} | grep Coef | grep "'${name}#" > $TFILE
idx=$(echo $(awk '{print $4}' $TFILE))
echo "${idx[@]//#}" > "${work_dir}/idx_${name}_Coef.1D"


# Tstat coeffs
3dinfo -verb ${input_file} | grep Tstat | grep "'${name}#" > $TFILE
idx=$(echo $(awk '{print $4}' $TFILE))
echo -e "${idx[@]//#}" > "${work_dir}/idx_${name}_Tstat.1D"


atlas_file=$(basename ${atlas})

# roistats

3dROIstats -overwrite -mask "${atlas}${extension}" "${input_file}[1dcat ${work_dir}/idx_${name}_Coef.1D]"  > "${work_dir}/${subject}_timecourses_${session}_${name}${prefix}_Coef${postfix}_${atlas_file}.txt"
3dROIstats -overwrite -mask "${atlas}${extension}" "${input_file}[1dcat ${work_dir}/idx_${name}_Tstat.1D]" > "${work_dir}/${subject}_timecourses_${session}_${name}${prefix}_Tstat${postfix}_${atlas_file}.txt"

rm $TFILE
