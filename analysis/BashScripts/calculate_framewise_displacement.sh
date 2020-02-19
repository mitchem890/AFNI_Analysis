#!/usr/bin/env bash

input=${1} 
output=${2} 


echo ${output}
echo ${input}

PI=3.1415926535897932384
# conversion_factor=$(echo "scale=10; ${PI}/180*50" | bc)	# for degrees to mm (as in HCP movement regressors)
conversion_factor=0.8726646250 	# because AFNI 1dmatcalc doesn't take a float < 1  without the leading 0!!! (oh, afni)

movfile="${input}/Movement_Regressors.txt" # the 12 column movement regressors file
echo ${movfile}

TFILE=$(mktemp)
trans=$(mktemp)
rot=$(mktemp)

sed 's/^[ \t]*//' ${movfile} > ${TFILE} # remove zeros at beginning of lines
1dcat ${TFILE}[6,7,8] > ${trans} # 0 based indexing
1dcat ${TFILE}[9,10,11] > ${rot}

		# rotation regressors conversion to mm and FD calculation

1dmatcalc "&read(${rot}) ${conversion_factor} * &write(${rot}_mm)"
1dcat -overwrite ${trans} ${rot}_mm > ${TFILE}
1deval -overwrite \
	-a ${TFILE}[0] \
	-b ${TFILE}[1] \
	-c ${TFILE}[2] \
	-d ${TFILE}[3] \
	-e ${TFILE}[4] \
	-f ${TFILE}[5] \
	-expr 'abs(a) + abs(b) + abs(c) + abs(d) + abs(e) + abs(f)' > "${output}_FD.txt"

echo "${output}_FD.txt"
# Creating censor list mask with FD threshold of 0.9 mm
1deval -expr 'within(a,0,0.9)' -a "${output}_FD.txt" > "${output}_FD_mask.txt"
chmod 750 "${output}_FD.txt" "${output}_FD_mask.txt"

rm ${TFILE} ${rot} ${trans}
