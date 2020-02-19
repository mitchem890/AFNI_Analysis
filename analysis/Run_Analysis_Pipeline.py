import logging
import os

import Analysis
import PreAnalysis
from classes import Images


# This is just an encapsulation of the two major parts of the analysis pipeline. PreAnalysis and Analysis
# This will also create a log file for each subject_wave_session_task
def create_logger(subject, wave, session, task, destination):
    logfilename = 'sub-' + str(subject) + '_' + wave + '_' + session + '_' + task + '_Analysis.log'  # Create a log file
    logfilename = os.path.join(destination, logfilename)  # place it in the output directory
    logging.basicConfig(level=logging.DEBUG, filename=logfilename, filemode='w',
                        format='%(message)s')  # Set the format of the log file name
    print(logfilename)
    logging.info('Running Subject ' + subject + '_' + wave + '_' + session + '_' + task)


def analysis_pipeline(origin, destination, events, wave, subject, session, task, pipeline, run_volume, run_surface,
                      run_preanalysis, run_analysis):
    create_logger(subject=subject, wave=wave, session=session, task=task, destination=destination)
    images = Images.get_images(origin=origin, subject=subject, wave=wave, session=session, task=task, pipeline=pipeline)

    if run_preanalysis:
        PreAnalysis.preAnalysis(destination, events, images, run_volume, run_surface)
    if run_analysis:
        Analysis.analysis(destination, images, run_volume, run_surface)
