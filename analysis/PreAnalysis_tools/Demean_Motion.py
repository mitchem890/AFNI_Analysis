import os
import sys
sys.path.append(os.path.abspath("/home"))

from classes import BashCommand


# Run Some Sick stats on the movement regressors
# This will get the trs for the image pair
# compute the enorm for motion
# demean_motion_parameters
# comput the derivatives of the motion parameters
#and create a censor list for the motion parameters
def demean_motion(origin, images):
    fullpath = os.path.join(origin, images[0].subject, 'INPUT_DATA', images[0].task, images[0].session)

    hcp_volume_image_run1 = f"tfMRI_{images[0].root_name}.nii.gz"
    hcp_volume_image_run2 = f"tfMRI_{images[1].root_name}.nii.gz"

    if os.path.isfile(os.path.join(fullpath, hcp_volume_image_run1)) and os.path.isfile(
            os.path.join(fullpath, hcp_volume_image_run2)):
        tr_count1 = BashCommand.get_tr_count(infile=os.path.join(fullpath, hcp_volume_image_run1)).run_command()
        tr_count2 = BashCommand.get_tr_count(infile=os.path.join(fullpath, hcp_volume_image_run2)).run_command()
        movreg6 = os.path.join(fullpath, 'movregs6.txt')

        #    log "TR counts ${subject} ${task} ${session} :\t" ${tr_count1} ${tr_count2} >> ${TLOG}
        command = BashCommand.compute_enorms(infile=movreg6,
                                             tr_count1=tr_count1,
                                             tr_count2=tr_count2,
                                             enormpath=os.path.join(fullpath, f'motion_enorm_{images[0].session}.1D'))
        print(f"{command} of {images[0]} and {images[1].encoding}")
        command.run_command()

        # compute de-meaned motion parameters (for use in regression)
        command = BashCommand.demean_motion_parameters(infile=movreg6,
                                                       tr_count1=tr_count1,
                                                       tr_count2=tr_count2,
                                                       demeanpath=os.path.join(fullpath,
                                                                               f"motion_demean_{images[0].session}.1D"))
        print(f"{command} of {images[0]} and {images[1].encoding}")
        command.run_command()

        # compute motion parameter derivatives (just to have)
        command = BashCommand.compute_motion_parameter_derivatives(infile=movreg6,
                                                                   tr_count1=tr_count1,
                                                                   tr_count2=tr_count2,
                                                                   derivpath=os.path.join(fullpath,
                                                                                          f'motion_deriv_{images[0].session}.1D')
                                                                   )
        print(f"{command} of {images[0]} and {images[1].encoding}")
        command.run_command()

        # censor list
        command = BashCommand.create_censor_list(infile=movreg6,
                                                 tr_count1=tr_count1,
                                                 tr_count2=tr_count2,
                                                 censor_list_file=os.path.join(fullpath, 'censor_list.1D'),
                                                 censorTR_file=os.path.join(fullpath, 'censor_data.1D')
                                                 )
        print(f"{command} of {images[0]} and {images[1].encoding}")
        command.run_command()
