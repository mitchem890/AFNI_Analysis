import os
import pandas as pd
import glob
from shutil import copyfile
import csv
import RunShellFunc as rs

#Split a given Cifti image into a left and right hemisphere gifti
def cifti_split(input, output):

    rs.run_shell_command("wb_command -cifti-separate "
                         + input + " COLUMN -metric CORTEX_LEFT "
                         + output + "_L.func.gii") #make gifti left hemisphere

    rs.run_shell_command("wb_command -cifti-separate "
                         + input + " COLUMN -metric CORTEX_RIGHT "
                         + output + "_R.func.gii")  # make gifti Right hemisphere


#For use with the HCP data. Calculate the FDs from the Movement regressors
def calculate_fd(input, output):
    rs.run_shell_command("bash /home/calculate_framewise_displacement.sh" +
                         " " + input +
                         " " + output)
                          # Calculate and place both the FD.txt and FD_mask.txt


#Calculate the DVARS from the Nifti for use with HCP data WARNING NOT CONFIRMED working
def calculate_dvars(nifti, output):
    # Creating standardized DVARS (from Tom Nichols' code)
    # output should look like "${series}/${subjects}_${name}_DVARS.txt"

    rs.run_shell_command("bash /home/dvars_nichols.sh " +
                         nifti +
                         " " + output)

#Pull the movement regressors out of fmriprep tsv for use with the fmriprep output
def make_movement_regressors(input, output):

    motion = pd.read_csv(input, delimiter='\t', encoding='utf-8')

    data = {'trans_x': motion['trans_x'], 'trans_y': motion['trans_y'], 'trans_z': motion['trans_z'],
            'rot_x': motion['rot_x'], 'rot_y': motion['rot_y'], 'rot_z': motion['rot_z']}
    df = pd.DataFrame(data=data)
    df = df[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
    df.to_csv(output, sep='\t', header=False, index=False, quoting=csv.QUOTE_NONE, float_format='%.8f')


#Pull the FD out of fmriprep tsv for use with the fmriprep output
def make_fd(input, output):

    motion = pd.read_csv(input, delimiter='\t', encoding='utf-8')
    data = {'framewise_displacement': motion['framewise_displacement']}
    df = pd.DataFrame(data=data)
    df.iloc[0] = 0
    df.round(5)
    df.to_csv(output, sep='\t', header=False, index=False, quoting=csv.QUOTE_NONE, float_format='%.8f')


#Pull the DVARS out of fmriprep tsv for use with the fmriprep output
def make_dvars(input, output):
    motion = pd.read_csv(input, delimiter='\t', encoding='utf-8')
    data = {'std_dvars': motion['std_dvars']}
    df = pd.DataFrame(data=data)
    df.iloc[0] = 0
    df.round(5)
    df.to_csv(output, sep='\t', index=False, header=False, quoting=csv.QUOTE_NONE, float_format='%.8f')

#Create the FD mask with a threshold of .9 for use with the fmriprep output
def make_fd_mask(input, output):
    data = rs.run_shell_command("1deval -expr 'within(a,0,0.9)' -a " + input, return_output=True)
    with open(output, 'w') as f:
        for i in data:
            f.write(i+'\n')

#resample the nifti image to fit to what is expected out of the hcp pipeline. for use with fmriprep
def resample(input, output):
    rs.run_shell_command("3dresample -master /home/atlases/gordon_2p4_resampled_wsubcort_LPI.nii.gz" +
                         " -input " + input +
                         " -prefix " + output)
    if os.path.exists(output):
        os.remove(input)
        os.rename(output, input)
    else:
        print("3dResample Failed")

#Check to make sure there are no blank evts for use with both fmriprep and hcp
def check_evts(input):
    files = os.listdir(input)
    for file in files:
        for line in file:
            if len(line.strip().strip('*')) == 0:
                print('found empty line in file ' + str(file))



#check the evts for blanks
#grab the correct evts
#calculate the FD
#Calculate the DVAR
#Split the Cifti into Gifti's
#Copy the Nifti to the Results
#Copy the Movement regressors to the results
def copy_input_data_hcp(subject, wave, session, task, encoding, runNum, origin, destination, events):
    print("Copying Data for " + subject + " " + session + " " + task + "run: " + runNum)
    origin=os.path.join(origin,subject,'MNINonLinear', 'Results', 'tfMRI_'+task.title()+session[0:3].title()+runNum+'_'+encoding) #Where the Data is found
    task_dest = os.path.join(destination, subject, 'INPUT_DATA', task, session) #Where the data is going
    hcp_volume_image = "tfMRI_" + task + session[0:3].title() + runNum + '_' + encoding + '.nii.gz' #Nifti Volume image
    hcp_cifti_image = 'tfMRI_'+task.title()+session[0:3].title()+runNum+'_'+encoding+"_Atlas.dtseries.nii" #Cifti image name
    hcp_surface_image='tfMRI_' + task + session[0:3].title() + runNum + '_' + encoding
    hcp_surface_image_L = hcp_surface_image+ '_L.func.gii'
    hcp_surface_image_R = hcp_surface_image + '_R.func.gii'
    evt_dir = os.path.join(events, subject, 'evts')

    check_evts(evt_dir)
    #Get the correct evts
    for file in glob.glob(os.path.join(evt_dir, '*' + task + '*' + session + '*')):
        copyfile(file, os.path.join(task_dest, os.path.basename(file)))
    #create a name template
    name=subject+"_tfMRI_"+task.title()+session[0:3].title()+runNum+'_'+encoding

    print('Calculating FD of: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    calculate_fd(input=origin, output=os.path.join(task_dest, name))
    print('Calculating DVARs of: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    calculate_dvars(nifti=os.path.join(origin, hcp_volume_image), output=os.path.join(task_dest, name+"_DVARS.txt"))
    print('Splitting the Cifti into Gifti\'s: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    cifti_split(input=os.path.join(origin, hcp_cifti_image), output=os.path.join(task_dest, hcp_surface_image))

    if not os.path.exists(task_dest):
        os.mkdir(task_dest)
    copyfile(os.path.join(origin, hcp_volume_image), os.path.join(task_dest, hcp_volume_image))

    origin_hcp_movement_regressors='Movement_Regressors.txt'
    hcp_movement_regressors='Movement_Regressors_' + task + session[0:3].title() + runNum + '_' + encoding+'.txt'

    hcp_fd=subject+'_tfMRI_'+task + session[0:3].title() + runNum + '_' + encoding + '_FD.txt'
    hcp_dvars = subject + '_tfMRI_'+task + session[0:3].title() + runNum + '_' + encoding + '_DVARS.txt'
    hcp_fd_mask=subject+'_tfMRI_'+task + session[0:3].title() + runNum + '_' + encoding + '_FD_mask.txt'

    copyfile(os.path.join(origin, origin_hcp_movement_regressors), os.path.join(task_dest, hcp_movement_regressors))


#check the evts for blanks
#grab the correct evts
#copy the volume
#copy the surface images
#make the Movement regressors
#Make the DVARS
#make the fd masks
#Resample the volume image to fit hcp format
def copy_input_data_fmriprep(subject, wave, session, task, encoding, runNum, origin, destination, events):
    print("Copying Data for " + subject + " " + session + " " + task + "run: " + runNum)
    origin= os.path.join(origin,"sub-"+str(subject), "ses-"+wave+session[0:3].lower(),"func")
    task_dest = os.path.join(destination, subject, 'INPUT_DATA', task, session)

    fmriprep_volume_image = "sub-" + str(subject) + "_ses-" + str(wave) + str(session).lower()[0:3] +"_task-"+ str(task)\
                            +"_acq-mb4" + str(encoding) + "_run-"+ str(runNum) +\
                            "_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    hcp_volume_image = "tfMRI_" + task + session[0:3].title() + runNum + '_' + encoding + '.nii.gz'

    fmriprep_regressors = 'sub-' + subject + '_ses-' + str(wave) + str(session).lower()[0:3] + '_task-' + task + \
                          '_acq-mb4' + encoding + '_run-' + runNum +'_desc-confounds_regressors.tsv'


    fmriprep_surface_image_L="sub-" + str(subject) + "_ses-" + str(wave) + str(session).lower()[0:3] +"_task-"+ \
                             str(task) +"_acq-mb4" + str(encoding) + "_run-"+ str(runNum) +\
                             '_space-fsaverage5_hemi-L.func.gii'
    hcp_surface_image_L='tfMRI_' + task + session[0:3].title() + runNum + '_' + encoding + '_L.func.gii'

    fmriprep_surface_image_R = "sub-" + str(subject) + "_ses-" + str(wave) + str(session).lower()[0:3] + "_task-" + str(
        task) + "_acq-mb4" + str(encoding) + "_run-" + str(runNum) + '_space-fsaverage5_hemi-R.func.gii'

    hcp_surface_image_R='tfMRI_' + task + session[0:3].title() + runNum + '_' + encoding + '_R.func.gii'


    evt_dir = os.path.join(events,subject,'evts')

    print('Checking evts of: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    check_evts(evt_dir)
    for file in glob.glob(os.path.join(evt_dir,'*'+task+'*'+session+'*')):
        copyfile(file, os.path.join(task_dest, os.path.basename(file)))

    if not os.path.exists(task_dest):
        os.mkdir(task_dest)

    copyfile(os.path.join(origin, fmriprep_volume_image), os.path.join(task_dest, hcp_volume_image))
    copyfile(os.path.join(origin, fmriprep_surface_image_L), os.path.join(task_dest, hcp_surface_image_L))
    copyfile(os.path.join(origin, fmriprep_surface_image_R), os.path.join(task_dest, hcp_surface_image_R))

    hcp_movement_regressors='Movement_Regressors_'+ task + session[0:3].title() + runNum + '_' + encoding+'.txt'
    hcp_fd=subject+'_tfMRI_'+task + session[0:3].title() + runNum + '_' + encoding + '_FD.txt'
    hcp_dvars = subject + '_tfMRI_'+task + session[0:3].title() + runNum + '_' + encoding + '_DVARS.txt'
    hcp_fd_mask=subject+'_tfMRI_'+task + session[0:3].title() + runNum + '_' + encoding + '_FD_mask.txt'
    hcp_resampled_image = "tfMRI_" + task + session[0:3].title() + runNum + '_' + encoding + '_tmp.nii.gz'

    print('Making movement regressors of: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    make_movement_regressors(os.path.join(origin, fmriprep_regressors),os.path.join(task_dest, hcp_movement_regressors))
    print('Making Functional Displacement of: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    make_fd(os.path.join(origin, fmriprep_regressors),os.path.join(task_dest, hcp_fd))
    print('Making DVARS of: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    make_dvars(os.path.join(origin, fmriprep_regressors),os.path.join(task_dest, hcp_dvars))
    print('Making FD mask of: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    make_fd_mask(os.path.join(task_dest, hcp_fd), os.path.join(task_dest, hcp_fd_mask))
    print('Resampling: ' + subject + ' ' + wave + ' ' + session + ' ' + ' ' + task)
    resample(os.path.join(task_dest, hcp_volume_image), os.path.join(task_dest, hcp_resampled_image))




