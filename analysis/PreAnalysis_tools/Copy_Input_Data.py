import glob
from shutil import copyfile
import os
import sys

sys.path.append("..")  # Adds higher directory to python modules path.
from PreAnalysis_tools import Confounds_Regressors_Interface as cri
from classes import Images, BashCommand
from utils import logger


# Check to make sure there are no blank evts for use with both fmriprep and hcp
def check_evts(input, image):
    files = glob.glob(os.path.join(input, f"{image.subject}_{image.task}_{image.session}*txt"))

    GoodFiles = []

    for file in files:
        with open(os.path.join(input, file), "r") as a_file:
            for line in a_file:
                if len(line.strip().strip('*')) == 0:
                    print('found empty line in file ' + str(file))
                    logger.logger(f'Found blank evt {str(file)}', 'warning')
                    GoodFiles.append(False)
                else:
                    GoodFiles.append(True)
                if not any(GoodFiles):
                    print("All of the evts had issues")
                    logger.logger(f'ERROR: All evts were blank', 'error')
                    raise NameError(f'ERROR: All evts were blank for {image.subject} {image.session} {image.task}')


def copy_input_data(images, destination, events):
    for image in images:
        if image.pipeline == 'hcp':
            copy_input_data_hcp(image, destination, events)
        elif image.pipeline == 'fmriprep':
            copy_input_data_fmriprep(image, destination, events)


# This function will:
# Check the evts for blanks
# Calculate the FDs
# calculate the DVARS
# Split the Cifti into 2 giftis
# copy the nifti files over
# copy the movement regressor files over


def copy_input_data_hcp(image: Images.preprocessed_image, destination, events):
    print(f"Copying Data for {image}")
    origin = image.dirname  # Where the Data is found
    task_dest = os.path.join(destination, image.subject, 'INPUT_DATA', image.task,
                             image.session)  # Where the data is going

    hcp_volume_image = f"tfMRI_{image.root_name}.nii.gz"
    hcp_cifti_image = f"tfMRI_{image.root_name}_Atlas.dtseries.nii"  # Cifti image name
    evt_dir = os.path.join(events, image.subject, 'evts')

    check_evts(evt_dir, image)
    # Get the correct evts
    for file in glob.glob(os.path.join(evt_dir, '*' + image.task + '*' + image.session + '*')):
        copyfile(file, os.path.join(task_dest, os.path.basename(file)))

    # create a name template
    name = f"{image.subject}_tfMRI_{image.root_name}"

    command = BashCommand.calculate_fds(infile=origin, outfile=os.path.join(task_dest, name))
    print(f"{command} of {image}")
    command.run_command()

    command = BashCommand.calculate_dvars(infile=os.path.join(origin, hcp_volume_image),
                                          outfile=os.path.join(task_dest, f"{name}_DVARS.txt"))
    print(f"{command} of {image}")
    command.run_command()

    command = BashCommand.cifti_split(infile=os.path.join(origin, hcp_cifti_image),
                                      outfile=os.path.join(task_dest, f"tfMRI_{image.root_name}_L.func.gii"),
                                      metric="CORTEX_LEFT")
    print(f"{command} of {image}")
    command.run_command()

    command = BashCommand.cifti_split(infile=os.path.join(origin, hcp_cifti_image),
                                      outfile=os.path.join(task_dest, f"tfMRI_{image.root_name}_R.func.gii"),
                                      metric="CORTEX_RIGHT")
    print(f"{command} of {image}")
    command.run_command()

    if not os.path.exists(task_dest):
        os.mkdir(task_dest)
    # only copy the file over if it doesnt exist and the afni_ready image doesnt exist
    if not (os.path.exists(image.afni_ready_volume_file) or os.path.exists(os.path.join(task_dest, hcp_volume_image))):
        copyfile(os.path.join(origin, hcp_volume_image), os.path.join(task_dest, hcp_volume_image))

    origin_hcp_movement_regressors = "Movement_Regressors.txt"

    copyfile(os.path.join(origin, origin_hcp_movement_regressors),
             os.path.join(task_dest, image.movement_regressor))


# check the evts for blanks
# grab the correct evts
# copy the volume
# copy the surface images
# make the Movement regressors
# Make the DVARS
# make the fd masks
# Resample the volume image to fit hcp format

#Find the multiband factor according to fmriprep
def find_multiband_factor(image):
    fmriprep_root_name = f"sub-{str(image.subject)}_ses-{str(image.wave)}{str(image.session).lower()[0:3]}_task-{str(image.task)}_acq-mb?{str(image.encoding)}_run-{str(image.run_num)}"
    fmriprep_volume_image = f"{fmriprep_root_name}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"

    multiband_factor=glob.glob(os.path.join(image.dirname, fmriprep_volume_image))[0].split('mb')[-1][0]

    return multiband_factor


def copy_input_data_fmriprep(image, destination, events):
    print(f"Copying Data for {image.subject} {image.session} {image.task} run: {image.run_num}")
    task_dest = os.path.join(destination, image.subject, 'INPUT_DATA', image.task, image.session)
    multiband_factor = find_multiband_factor(image)
    fmriprep_root_name = f"sub-{str(image.subject)}_ses-{str(image.wave)}{str(image.session).lower()[0:3]}_task-{str(image.task)}_acq-mb{str(multiband_factor)}{str(image.encoding)}_run-{str(image.run_num)}"
    fmriprep_volume_image = f"{fmriprep_root_name}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"

    fmriprep_regressors = f"{fmriprep_root_name}_desc-confounds_regressors.tsv"
    fmriprep_surface_image_L = f"{fmriprep_root_name}_space-fsaverage5_hemi-L.func.gii"
    fmriprep_surface_image_R = f"{fmriprep_root_name}_space-fsaverage5_hemi-R.func.gii"

    hcp_root_name = f"tfMRI_{image.task}{image.session[0:3].title()}{image.run_num}_{image.encoding}"
    hcp_volume_image = f"{hcp_root_name}.nii.gz"
    hcp_surface_image_L = f"{hcp_root_name}_L.func.gii"
    hcp_surface_image_R = f"{hcp_root_name}_R.func.gii"

    evt_dir = os.path.join(events, image.subject, 'evts')

    print(f'Checking evts of: {image.subject} {image.wave} {image.session} {image.task}')
    check_evts(evt_dir, image)
    for file in glob.glob(os.path.join(evt_dir, '*' + image.task + '*' + image.session + '*')):
        copyfile(file, os.path.join(task_dest, os.path.basename(file)))

    if not os.path.exists(task_dest):
        os.mkdir(task_dest)

    hcp_fd = f"{image.subject}_{hcp_root_name}_FD.txt"
    hcp_dvars = f"{image.subject}_{hcp_root_name}_DVARS.txt"
    hcp_fd_mask = f"{image.subject}_{hcp_root_name}_FD_mask.txt"

    print(f"Making movement regressors of: {image.subject} {image.wave} {image.session} {image.task}")
    cri.get_movement_regressors(os.path.join(image.dirname, fmriprep_regressors),
                                os.path.join(task_dest, image.movement_regressor))
    print(f"Making Functional Displacement of: {image.subject} {image.wave} {image.session} {image.task}")
    cri.get_fd(os.path.join(image.dirname, fmriprep_regressors), os.path.join(task_dest, hcp_fd))
    print(f"Making DVARS of: {image.subject} {image.wave} {image.session} {image.task}")
    cri.get_dvars(os.path.join(image.dirname, fmriprep_regressors), os.path.join(task_dest, hcp_dvars))
    print(f"Making FD mask of: {image.subject} {image.wave} {image.session} {image.task}")
    cri.make_fd_mask(os.path.join(task_dest, hcp_fd), os.path.join(task_dest, hcp_fd_mask))

    # afni_ready_volume = lpi_scale_blur*nii.gz, hcp_volume_image=tfMRI*.nii.gz
    # Situation Fresh Run
    # in the INPUT_DATA there will be nothing.
    # hcp_volume_image does not exist and afni_ready_image does not exist
    # Copy data

    # Situation Interupted Run in preanalysis:
    # in INPUT_DATA there will be hcp_volume image
    # afni_ready_image does not exist
    # do nothing
    # Situation Interupted Run in analysis:
    # in INPUT_DATA there will be afni_ready_image
    # hcp volume image does not exist
    # do nothing
    if not (os.path.exists(os.path.join(task_dest, image.afni_ready_volume_file)) or os.path.exists(
            os.path.join(task_dest, hcp_volume_image))):
        print(f"Resampling: {image.subject} {image.wave} {image.session} {image.task}")
        BashCommand.resample(infile=os.path.join(image.dirname, fmriprep_volume_image),
                             outfile=os.path.join(task_dest, hcp_volume_image),
                             voxel_dim=image.voxel_dim).run_command()

    if not (os.path.exists(os.path.join(task_dest, image.get_afni_ready_surface_file('L'))) or os.path.exists(
            os.path.join(task_dest, hcp_surface_image_L))):
        copyfile(os.path.join(image.dirname, fmriprep_surface_image_L), os.path.join(task_dest, hcp_surface_image_L))

    if not (os.path.exists(os.path.join(task_dest, image.get_afni_ready_surface_file('R'))) or os.path.exists(
            os.path.join(task_dest, hcp_surface_image_R))):
        copyfile(os.path.join(image.dirname, fmriprep_surface_image_R), os.path.join(task_dest, hcp_surface_image_R))
