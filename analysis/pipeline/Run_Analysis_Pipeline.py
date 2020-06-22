
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from pipeline import Analysis, PreAnalysis, OutputVerifier
from classes import Images
from utils import logger

def update_image_properties(image, destination):
    logger.logger(f'Updating Image Dimensions', 'info')
    afni_ready_image = os.path.join(destination, image.subject, 'INPUT_DATA', image.task, image.session,
                                    image.afni_ready_volume_file)
    image.set_voxel_dim(afni_ready_image)
    image.set_image_dim(afni_ready_image)


def create_logger(subject, wave, session, task, destination):
    logfilename = f'sub-{str(subject)}_{wave}_{session}_{task}_Analysis.log'  # Create a log file
    logfilename = os.path.join(destination, logfilename)  # place it in the output directory
    logger.setup_logger(logfilename)
    print(logfilename)
    logger.logger(f'Running Subject {subject}_{wave}_{session}_{task}', 'info')


def analysis_pipeline(origin, destination, events, wave, subject,
                      session, task, pipeline, run_volume,
                      run_surface, run_preanalysis, run_analysis):
    create_logger(subject=subject, wave=wave, session=session, task=task, destination=destination)
    images = Images.get_images(origin=origin, subject=subject, wave=wave, session=session, task=task, pipeline=pipeline)

    if run_preanalysis:
        PreAnalysis.preAnalysis(destination, events, images, run_volume, run_surface)
    for image in images:
        update_image_properties(image, destination)
        
    if run_analysis:
        GLM_set = Analysis.analysis(destination, images, run_volume, run_surface)

    #Check Files!
    OutputVerifier.outputVerifier(images=images, GLM_set=GLM_set)