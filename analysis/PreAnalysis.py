import Copy_Input_Data
import Format_Motion_Regressors
import Demean_Motion
import Surface_Demean_Images
import Volume_Demean_Images
import glob
import os

encodings = ['AP', 'PA']
hemispheres = ['L', 'R']

#Find the Correct run number for a given encoding. THIS has not been implemented for the HCP data. HCP ASSUMES 1_AP and 2_PA
def find_correct_run_number(origin, wave, subject, session, task, encoding, pipeline):



    if pipeline == 'fmriprep':
        origin = os.path.join(origin, "sub-" + str(subject), "ses-" + wave + session[0:3].lower(), "func")

        print("RunNumber: ")

        files = glob.glob(os.path.join(origin, 'sub-' + subject + '_ses-' + wave +
                                       session[0:3].lower() + '_task-' + task.title()
                                       + '_acq-mb*' + encoding
                                       + '_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'))
        print(os.path.join(origin, 'sub-' + subject + '_ses-' + wave +
                                       session[0:3].lower() + '_task-' + task.title()
                                       + '_acq-mb*' + encoding
                                       + '_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'))
        runNum = os.path.basename(files[0]).split('run-')[1][0]  # Get the run number from the file name
        # / scratch / mjeffers / DMCCPILOT / PREPROC / 672756 / MNINonLinear / Results / rfMRI_RestBas1_AP/rfMRI_RestBas1_AP.nii.gz
    elif pipeline == 'hcp':
        #TODO add hcp sourcing of run num
        if encoding == 'AP':
            runNum='1'
        else:
            runNum='2'

    return runNum


# This Contains all the Preanalysis Steps of:
# CopyInputData
# Format Motion Regressors
# Demean Motion Regressors
# Demean Volume and Surface images
run_preanalysis=True
def preanalysis(origin, destination, events, wave, subject, session, task, pipeline, run_volume, run_surface):
    if run_preanalysis:
        print("Running Preanalysis on: " + wave + ' ' + session + ' ' + task)

        if not os.path.exists(os.path.join(destination, subject, 'INPUT_DATA', task,
                                           session)):  # If there is no INPUT_DATA folder in the subject create it
            os.makedirs(os.path.join(destination, subject, 'INPUT_DATA', task, session))

        # For encodings AP and PA these must be processed seperatly
        for encoding in encodings:
            print(encoding)
            runNum = find_correct_run_number(origin, wave, subject, session, task, encoding, pipeline)
            print(runNum)
            if pipeline == 'hcp':

                Copy_Input_Data.copy_input_data_hcp(subject, wave, session, task, encoding, runNum, origin, destination,
                                                    events)

            elif pipeline == 'fmriprep':
                print("Copying Input Data: " + task)
                Copy_Input_Data.copy_input_data_fmriprep(subject, wave, session, task, encoding, runNum, origin,
                                                         destination, events)

        #This is independant of the encoding
        Format_Motion_Regressors.format_motion_regressors(destination, subject, session,
                                                          task)  # format the motion regressors
        Demean_Motion.demean_motion(destination, subject, session, task)  # Demean Motion

        #Demeaning the images must be done on each encoding
        for encoding in encodings:
            runNum = find_correct_run_number(origin, wave, subject, session, task, encoding, pipeline)

            if run_volume:
                Volume_Demean_Images.volume_demean_images(destination, subject, session, task, runNum,
                                                          encoding)  # Demean the volume images
            if run_surface:
                for hemisphere in hemispheres:
                    Surface_Demean_Images.surface_demean_images(destination, subject, session, task, runNum, encoding,
                                                                hemisphere)  # Demean the surface images
