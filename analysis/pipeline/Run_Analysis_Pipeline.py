import logging
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from pipeline import Analysis, PreAnalysis, OutputVerifier
from classes import Images

def create_logger(subject, wave, session, task, destination):
    logfilename = f'sub-{str(subject)}_{wave}_{session}_{task}_Analysis.log'  # Create a log file
    logfilename = os.path.join(destination, logfilename)  # place it in the output directory

    logging.basicConfig(level=logging.DEBUG, filename=logfilename, filemode='w',
                        format='%(message)s')  # Set the format of the log file name
    print(logfilename)
    logging.info(f'Running Subject {subject}_{wave}_{session}_{task}')


def analysis_pipeline(origin, destination, events, wave, subject,
                      session, task, pipeline, run_volume,
                      run_surface, run_preanalysis, run_analysis, strict_analysis):
    create_logger(subject=subject, wave=wave, session=session, task=task, destination=destination)
    images = Images.get_images(origin=origin, subject=subject, wave=wave, session=session, task=task, pipeline=pipeline)
    for image in images:
        print(f"Found {image}")
    if run_preanalysis:
        PreAnalysis.preAnalysis(destination, events, images, run_volume, run_surface, strict_analysis)
    if run_analysis:
        GLM_set = Analysis.analysis(destination, images, run_volume, run_surface, strict_analysis)

    #Check Files!
    OutputVerifier.outputVerifier(images=images, GLM_set=GLM_set)