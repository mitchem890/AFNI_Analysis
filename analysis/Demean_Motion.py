import os
import RunShellFunc as rs

#Run Some Sick stats on the movement regressors
def demean_motion(origin,subject,session,task):

    fullpath = os.path.join(origin, subject, 'INPUT_DATA',task, session)
    print(fullpath)
    #TODO Check for correct run number
    hcp_volume_image_run1="tfMRI_" + task + session[0:3].title() + '1_AP.nii.gz'
    hcp_volume_image_run2="tfMRI_" + task + session[0:3].title() + '2_PA.nii.gz'
    if os.path.isfile(os.path.join(fullpath, hcp_volume_image_run1)) and os.path.isfile(os.path.join(fullpath, hcp_volume_image_run2)):
        tr_count1=rs.run_shell_command("3dinfo -nv " + os.path.join(fullpath, hcp_volume_image_run1), return_output=True)
        tr_count2=rs.run_shell_command("3dinfo -nv " + os.path.join(fullpath, hcp_volume_image_run2), return_output=True)

#    log "TR counts ${subject} ${task} ${session} :\t" ${tr_count1} ${tr_count2} >> ${TLOG}
        print("Computing Motion Enorms: " + subject + ' ' + session + ' ' + ' ' + task)
        enormpath=os.path.join(fullpath, 'motion_enorm_'+ session + '.1D')
        rs.run_shell_command('1d_tool.py -infile ' + os.path.join(fullpath, 'movregs6.txt') +
                             ' -set_run_lengths ' + str(tr_count1) + " " + str(tr_count2) +
                             ' -derivative -collapse_cols euclidean_norm'+
                             ' -write ' + enormpath +
                             ' -overwrite')

# compute de-meaned motion parameters (for use in regression)
        print("Demeaning motion Parameters: " + subject + ' ' + session + ' ' + ' ' + task)
        demeanpath=os.path.join(fullpath,'motion_demean_' + session + '.1D')
        rs.run_shell_command('1d_tool.py -infile ' + os.path.join(fullpath,'movregs6.txt') +
                             ' -set_run_lengths ' + str(tr_count1) + " " + str(tr_count2) +
                             ' -demean' +
                             ' -write ' + demeanpath +
                             ' -overwrite')

# compute motion parameter derivatives (just to have)
        print("Computing Motion Parameter Derivatives: " + subject + ' ' + session + ' ' + ' ' + task)
        derivpath=os.path.join(fullpath, 'motion_deriv_' + session + '.1D')
        rs.run_shell_command('1d_tool.py -infile ' + os.path.join(fullpath,'movregs6.txt') +
                             ' -set_run_lengths ' + str(tr_count1) + " " + str(tr_count2) +
                             ' -derivative' +
                             ' -demean' +
                             ' -write ' + derivpath +
                             ' -overwrite')

# censor list
        print("Creating Censor List: "+ subject + ' ' + session + ' ' + ' ' + task)
        rs.run_shell_command('1d_tool.py -infile ' + os.path.join(fullpath,'movregs6.txt') +
                             ' -set_run_lengths ' + str(tr_count1) + " " + str(tr_count2) +
                             ' -derivative' + ' -censor_prev_TR' +
                             ' -collapse_cols euclidean_norm' +
                             ' -moderate_mask -0.3 0.3' +
                             ' -write ' + os.path.join(fullpath, 'censor_list.1D') +
                             ' -write_CENSORTR ' + os.path.join(fullpath, 'censor_data.1D') +
                             ' -verb 0' +
                             ' -overwrite')

#   1d_tool.py - infile "${in_dir}/movregs6.txt" \
#   -set_run_lengths "${tr_count1}" "${tr_count2}" \
#   -derivative  \
#   -collapse_cols euclidean_norm \
#   -moderate_mask -0.3 0.3 \
#   -write "${in_dir}/censor_list.1D" \
#   -write_CENSORTR "${in_dir}/censor_data.1D" \
#   -verb 0 \
#   -show_censor_count 1 > "${in_dir}/censor_count.txt" \
#   -overwrite