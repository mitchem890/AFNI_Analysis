import os

import Format_Motion_Regressors
import Copy_Input_Data
import Demean_Images
import Demean_Motion

hemispheres = ['L', 'R']


# This Contains all the Preanalysis Steps of:
# CopyInputData
# Format Motion Regressors
# Demean Motion Regressors
# Demean Volume and Surface images
def preAnalysis(destination, events, images, run_volume, run_surface):
    print(f"Running Preanalysis on: {images[0]} and {images[1].encoding}")

    # If there is no INPUT_DATA folder in the subject create it
    if not os.path.exists(
            os.path.join(destination, images[0].subject, 'INPUT_DATA', images[0].task, images[0].session)):
        os.makedirs(os.path.join(destination, images[0].subject, 'INPUT_DATA', images[0].task, images[0].session))
    ##TODO For images outside
    Copy_Input_Data.copy_input_data(images, destination, events)
    Format_Motion_Regressors.format_motion_regressors(destination, images)  # format the motion regressors
    Demean_Motion.demean_motion(destination, images)  # Demean Motion

    if run_volume:
        Demean_Images.volume_demean_images(destination, images)  # Demean the volume images
    if run_surface:
        for hemisphere in hemispheres:
            Demean_Images.surface_demean_images(destination, hemisphere, images)  # Demean the surface images
