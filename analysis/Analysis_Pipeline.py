import logging
import PreAnalysis
import Analysis
import os


#This is just an encapsulation of the two major parts of the analysis pipeline. PreAnalysis and Analysis
#This will also create a log file for each subject_wave_session_task
def analysis_pipeline(origin, destination, events, wave, subject, session, task, pipeline, run_volume, run_surface,
                      run_preanalysis, run_analysis):
    logfilename = 'sub-' + str(subject) + '_' + wave + '_' + session + '_' + task + '_Analysis.log'  # Create a log file
    logfilename = os.path.join(destination, logfilename)  # place it in the output directory
    logging.basicConfig(level=logging.DEBUG, filename=logfilename, filemode='w',
                        format='%(message)s')  # Set the format of the log file name
    print(logfilename)
    logging.info('Running Subject ' + subject + '_' + wave + '_' + session + '_' + task)

    print(run_preanalysis)
    print(run_analysis)
    #if run_preanalysis:
    PreAnalysis.preanalysis(origin, destination, events, wave, subject, session, task, pipeline, run_volume, run_surface)
    #if run_analysis:
    Analysis.analysis(destination, wave, subject, session, task, pipeline, run_volume, run_surface)
