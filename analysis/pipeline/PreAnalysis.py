import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from PreAnalysis_tools import Copy_Input_Data, Format_Motion_Regressors, Demean_Images, Demean_Motion, Run_Splitter
from utils import logger
hemispheres = ['L', 'R']


# This Contains all the Preanalysis Steps of:
# CopyInputData
# Format Motion Regressors
# Demean Motion Regressors
# Demean Volume and Surface images
def preAnalysis(destination, events, images, run_volume, run_surface):
    try:
        print(f"Running Preanalysis on: {images[0]} and {images[1].encoding}")

        # If there is no INPUT_DATA folder in the subject create it
        if not os.path.exists(
            os.path.join(destination, images[0].subject, 'INPUT_DATA', images[0].task, images[0].session)):
            os.makedirs(os.path.join(destination, images[0].subject, 'INPUT_DATA', images[0].task, images[0].session))

        ##TODO For loop of images outside
        Copy_Input_Data.copy_input_data(images, destination, events)
        Format_Motion_Regressors.format_motion_regressors(destination, images)  # format the motion regressors
        Demean_Motion.demean_motion(destination, images)  # Demean Motion
        Run_Splitter.find_and_split_evts(os.path.join(destination, images[0].subject, 'INPUT_DATA', images[0].task, images[0].session), images)
        Run_Splitter.find_and_split_movement(os.path.join(destination, images[0].subject, 'INPUT_DATA', images[0].task, images[0].session), images)
        if run_volume:
            Demean_Images.volume_demean_images(destination, images)  # Demean the volume images
        if run_surface:
            for hemisphere in hemispheres:
                Demean_Images.surface_demean_images(destination, hemisphere, images)  # Demean the surface images
    except Exception as e:
        print(e)
        print(f"Error Running Preanalysis")
        logger.logger(e, 'error')