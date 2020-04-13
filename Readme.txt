
#Testing new chunks of python code with containers:
#My basic process:
#1.Shell into image with both my code that I want to test and the data I want to test it on mounted
#2.navigate to where the code that you want to be tested is located
#3.run python
#4.import the important stuff that you will use
#5.run the command within python to launch the code
#6.look at results check errors
#7.edit code and run again Note will will have to exit the python instance and reload python for your changes to take place

#How I would do this on my local machine:
#assume my data lives here:
#/my/data/location/
#Assume my code That I want to test lives here:
#/home/mitchell/R01/Mitch/dockerprojects/AfniAnalysis/
singularity shell -B  /home/mitchell/R01/Mitch/dockerprojects/AfniAnalysis/:/testing/ -B /my/data/location/:/mnt/ afni_analysis.simg
#you will then be thrown into a shell for that container
cd /testing/analysis
python
#you should now be in a python shell
from pipeline import Run_Analysis_Pipeline
from config import globals
from utils import setup
setup.setup_environment()
globals.set_overwrite(False)
Run_Analysis_Pipeline.analysis_pipeline(origin='/mnt/LabWork/HCP_OUTPUT', destination='/mnt/LabWork/Afni_Analysis/', events='/mnt/LabWork/onsets', wave='wave1', subject='150423',session='baseline', task='Axcpt', pipeline='hcp', run_volume=True,run_surface=True, run_preanalysis=True, run_analysis=True)


##########Checking for missing files!########
#Depending on how you want to do this. 
#you may want to check the Files that were input into the analysis pipeline, and the Files that were output by the pipeline
#The way you could check the output files of the pipeline is by using the output of task GLMs,
#Specifically the roistats output, since this is the last file produced by the pipeline.
#A way to access this data would be through GLM_set.glms[0][0].roistats[0].roistats.outfile and GLM_set.glms[0][0].roistats[0].roistats.working_dir
#Where the GLM_set is the output of a call to TaskGLMs. Check out the Analysis.py File to see an implementation. also Note that the GLM_set is returned from the Analysis.py file
#so you should be able to use this in your file

#Before jumping into this it may be useful to take an hour or so and look through the top level code of the Afni_analysis container
#Ill give a brief outline of each file here but It would help if you follow along in the code
#before beginning get the latest version of the code from git hub
#Also build the latest version of the singularity image
#


#File Break down from the beginning of the Pipeline to the end

##########run.py
#This kicks off the whole pipeline. 
#it will read in user input and verify it using the Validate_User_Input python file
#it will also set the global variable of 'overwrite' this needs to be verified its working  
#This will then set up the multiprocessing so that multiple instances of the pipeline can run at the same time

##########Validate_user_input
#This will go through each of the inputs from the user and make sure that they are valid. if the user input a non-valid instuction. it will shut down and throw an error

##########globals.py
#Right now this is only used to house the overwite variable which should tell the pipeline to overwite any thing that it finds

#Run_Analysis_Pipeline.py
#This has 4 main functions:
#Create a logger to log the bash commands ran for a particular task
#find the images for that task using the Images.py class
#Run the Preanalysis
#Run the Analysis

##########Images.py
#This houses 3 functions
#1 super class 
#2 sub classes

#get_images 
#This function will simply pass off the information about a task to the correct function depending on the pipeline
#Returns a list of image objects

#get_images_fmriprep
#This function will use the glob functionality to search for images that match the fmriprep file naming structure
#After finding files that match the glob it will create image objects using fmriprep_preprocessed_image
#Returns a list of Images

#get_images_hcp
#This function will use the glob functionality to search for images that match the hcp file naming structure
#After finding files that match the glob it will create image objects using hcp_preprocessed_image
#Returns a list of Images


#Super Class
#preprocessed_image
#This is a class thats purpose is just to round up infor mation about the image
#This makes info about the image easier to pass off between futions later on
#you dont need to know about every attribute with in the class but it maybe usefuule to glance over them quickly to get a sense of what they hold

#Sub class
#class fmriprep_preprocessed_image(preprocessed_image):
#This is an instance of the preprocessed image class
#The reasons I built out subclasses is because the information about the image is found in different places in the file name depending on the preprocessing pipeline it was run through


#Sub class
#class hcp_preprocessed_image(preprocessed_image):
#Again This is an instance of the preprocessed image class build specifically for the hcp file name structure
#The reasons I built out subclasses is because the information about the image is found in different places in the file name depending on the preprocessing pipeline it was run through

##########PreAnalysis.py
# This Contains all the Preanalysis Steps of:
# Copy Input Data
# Format Motion Regressors
# Demean Motion Regressors
# Demean Volume and Surface images


##########Copy_Input_Data.py
#This purose of this is to mve the input data from the location given by origin to the ouput loaction given by destination
#This contains 4 functions



#copy_input_data(images, destination, events):
#This function simply handles the incoming data and routes it to the correct function depending on if its fmriprep or HCP

#copy_input_data_hcp(image: Images.preprocessed_image, destination, events)
#This function will:
#Check the evts for blanks
#Calculate the FDs
#calculate the DVARS
#Split the Cifti into 2 giftis
#copy the nifti files over
#copy the movement regressor files over
#almost all of this functionality is done in the bash excluding the copying and checking for blank evts



# copy_input_data_fmriprep(image, destination, events):
# check the evts for blanks
# grab the correct evts
# copy the volume
# copy the surface images
# make the Movement regressors
# Make the DVARS
# make the fd masks
# Resample the volume image to fit hcp format
# unlike copy_input_data_hcp The dvars and fds are already created by fmriprep and are stored in the confounds regressor file in the output of fmriprep 
# the only thing that we need to get them is to search through the counfounds regressors we will do this using the confounds_regressors_interface.py
# Because frmiprep outputs volume images in a different they must be resampled to fit the hcp templates later on
# This is done using a bash command

# check_evts
#this function will iterate through all the given evts and check for empty lines. and print that it has found an empty line in file name
#blank lines in evts are often unintentional but sometime can be intentional. Check with RAs when a blank line is seen in the evts


#Confounds_regressors_interface.py
#The purpouse of this file is to parse through the ouput confounds regressors of the fmriprep data.
#it contains 4 functions

#get_movement_regressors(input, output)
#This expects the coundfounds regressors file as the input and will write out the movement regressors as the output
# If this starts failing it may be that fmriprep has updated their headers on the confounds regressors. you may want to check that

#get_fd(input, output)
#This expects the coundfounds regressors file as the input and will write out the fds as the output
# If this starts failing it may be that fmriprep has updated their headers on the confounds regressors. you may want to check that

#get_dvars(input, output)
#This expects the coundfounds regressors file as the input and will write out the dvars as the output
#If this starts failing it may be that fmriprep has updated their headers on the confounds regressors. you may want to check that

#make_fd_mask(input, output):
#This expects a fd as an input and will output the fd_mask file
#The fd mask file will have a list of ones (include) or 0 (exclude) for each frame of the image. This tells the glm what to include and exclude


##########BashCommand.py
#This file contains a bunch of functions that will build out bash commands for the shell to run.
#ther is one super class and a bunc of subclasses.

#bash_command(object):
#This is the super class to every other function in here
#if has 2 basic things that is does
# it checks to see if the outfile exists for a command
#if it doesnt then it will pass the command to the shell and the command


#The rest of the functions will simply build out a shell command



##########Format Motion Regressors.py
#The purpose of this file is to format the motion regressors that were built.
#it takes the motion regressors from the first run and the second run and concatenates them together to make a single long file
#it does the same for the FD's and the fd masks

#format_motion_regressors
#This will round up all the names for the files we want to concatenate and pass them to the append function
#it will also get the first six colums of the motion regressors, because the others arent used


#append 
#will just concatenate a list of files together and write it to outfile


##########Demean_Motion.py
#This file will comput different statistics for the movement regressors. these computations are usually used for graphing purposes by Jo
#Some of them are used by the glm later on
#These are the calculations thate are done
# This will get the trs for the image pair
# compute the enorm for motion
# demean_motion_parameters
# comput the derivatives of the motion parameters
# and create a censor list for the motion parameters
#each of these are done in a bash call From BashCommands.py


##########Demean_Images.py
#This is the final step of the pre analyis it will get the images ready to go into glms
#There are multiple things that must be done to get the image ready for the glms
#This has 5 functions
#volume_demean_pipeline
#surface_demean_pipeline
#volume demean images
#surface demean images
#cleanup

#Volume Demean images will check to see if the final image has already been produced then is will use volume _demean_pipeline to build out a small demean pipeline to run the images through
#After running the images through each step of the pipeline it will clean it up using the cleanup function

#Surface_Demean_Images
#Works the same way as the volume demean images


#volume_demean_images_pipeline(image, fullpath):
#This will build out a pipeline to 
#AutoMask the images 
#BlurToFWHM
#calculate the mean using Tstat 
#deamean the images using calc
#Reorient the images to LPI
#Returns a list of commands


#surface_demean_images_pipeline(image, fullpath):
#This will build out a pipeline to 
#calculate the mean using Tstat 
#deamean the images using calc
#Returns a list of commands

#cleanup
#This will remove the temp files from the pipeline runs

#########Analysis.py
#This function file will take in your images and creat a glm set for them
#There is Get_Glms function
#analysis
#run_surface_glms
#run_volume_glms

#The analysis function is the main function that passes off to the other functions

#get_GLMs
#This function will take in images and 
#return the glms for a particular task. This will get the list from the classes TaskGLMs

#run_volume_glms 
#This will run the volume by iterating through the GLMs which are stored in a list of tuples with a structure like this:
#GLMs[(Volume_GLM1,Surface_L_GLM1,Surface_R_GLM1),(Volume_GLM2,Surface_L_GLM2,Surface_R_GLM2)...(Volume_GLMn,Surface_L_GLMn,Surface_R_GLMn)]
#Each of these GLMs will have a property called '.deconvolve' and '.remlfit' that represent the 3dDeconvolve and 3dRemlfit commands respectively
#Each GLM has multiple roistats that are iterated through and ran as well

#run_surface_glms
#works the same as run_volume_glms except it goes through each of the hemispheres



###########TaskGLMs.py
#The purpose of this file is to create a collection of GLMs for each task that is expected in the normal DMCC process
#it contains 
#1 super class
#4 subclasses
 
#TaskGLMs
#This is the super class it is the most generalized version of the GLMs

##generate_censor
#This willcreate a censor file based on the images used to create the TaskGLMs

##generate_ortvec
#This will create an othoganal vector based on the images used to create TaskGLMs

##build_glms
#This function will take in information and build out 3 glms store them in a tuple and return the tuple
#it takes in glm type which will almost always fall into the catagory of one of the following (ON_BLOCKS/ON_MIXED/EVENTS/HRF_EVENTS)
#it will take in a GLM Label which will be a subcategory of the EVENTS so for Axcpt the possible labels are (Buttons/Cues)
#it takes in a list of tuples called regressors_models_labels. This is a tuple of the regressor (file names, the models that we want to use on the regressors, and the labels for the regressors)
#it takes in contrasts_labels which is a tuple of (the contrast of the regressor we want to look at, label of that contrast)
#it also takes in a tuple roistats_designs_postfixes which is a tuple that contains the label of which subbrick to look at as well as a postfix to tag the name of the ouput file with. 
##The label is one of the labels from contrasts_labels, and regressors_models_labels which will identify the subrict to get the stats from in the output file
##The postfix is just a tag to describe the model that was ran on the regressor
#this function also set the force_tr for the surface GLMs based upon the MB of the runs


#create_on_blocks_glms
#The onblocks are the same across the tasks so this function will build the onblocks glms

#create_on_mixed_glms
#This function will create the on mixed glm which is (for the most part) the same across tasks the only thing that differs is the event model. This is substituted out by the subclasses

#generate_roistats_designs_postixes
#This function will generate the tuple roistats designs postfixes.
#This is composed of the labels of the contrasts and the regressors as well as a desctiption of the model that is used. that description will be used when ouputting the file

#AxcptGLMs
#This is a subclassof TaskGLMs
#create_cues_events_glm this is a function will create an Events Cues glm and pass back a tuple of GLMs
#create events GLMs collects all the event glms for the task this pattern is the same through out the rest of the Tasks



 
##########GLMs.py
#This file generalizes the glms. 
# a glm contains 2 parts. A 3dDeconvolve and a remlfit call. These 2 call makeup.
# a glm also contains multiple roistats.
# There is one super class that is just labeled GLM
# There are 2 subclasses one for volume and one for surface.
# 

#GLMs 
#This will gather all the parameters for the glms so that it can be passed to the bash command
# add_path_regressors_models_labels(self):
# This will add the correct path to the regressors that were placed in the regressors_models_labels
# generate_regressor_file_name(self, regressor):
# This will add the full file name to the regressors
# generate_output_dir(self):
# This will use info to create the output directory
# generate_roistats(self):
# This will create the roistats for the glms using thr roistats.py function
# __str__(self):
# This will make the GLM output info about itself 

#Volume_glm
#This is a subclass of glm
#The main difference is that it has its own default parameters
#It also generates its own input files nameing

##########Roistats.py
#The roistats class is a class built to gether the info of an roistats call in the BashCommands file


# build_roistats
# This will add the take the standard inputs
# to the roistats minus the atlas and extension
# it will return a list of roistats objects, 
# two for each atlas available a Tstas one and a Coef one





