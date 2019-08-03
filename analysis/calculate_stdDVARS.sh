
#!/bin/bash
while getopts i: option; do
    case "${option}" in
        i) input_dir=${OPTARG};; #The input stats file that we will be using to get all the data out. Should include directory path
        o) output_dir=${OPTARG};; #The output FD and FD mask file without the
        s) subject=${OPTARG};; #The subject number
        n) name=${OPTARG};; #The name that will be used in the output file ${subject}_${name}_FD.txt

    esac
done


if [[ -z "${subjects}" || "${origin}" ]]; then
    usage && error_exit "One or more mandatory parameters are empty"
fi

# -----

for subject in $subjects; do

    echo -e "\nSUBJECT\t:\t${subject}\n"
    in_dir="${data_dir}/${subject}/MNINonLinear/Results/"
    series_list=$(find ${in_dir} -mindepth 1 -maxdepth 1 -type d)

    for series in ${series_list}; do

	name=$(basename ${series})
	niifile="${series}/${name}.nii.gz"
	echo -e "\t${name}"

	if [[ -e "${niifile}" ]]; then
	    batch_job="dvars_${name}"



############## HERE FILE ##############
	    cat > ${batch_job}.pbs <<EOF

#!/bin/bash
#PBS -l nodes=1:ppn=1,mem=5gb,vmem=5gb,walltime=1:00:00
#PBS -N ${batch_job}
#PBS -W umask=0027
#PBS -j oe
#PBS -o ${batch_job}.log

module load fsl-5.0.11

# Creating standardized DVARS (from Tom Nichols' code)
/home/ccp_hcp/analysis/dvars_nichols.sh "${niifile}" "${series}/${subjects}_${name}_DVARS.txt"
chmod 750 "${series}/${subject}_${name}_DVARS.txt"