import argparse
import multiprocessing as mp
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import globals
from pipeline import Run_Analysis_Pipeline, AuxAnalysis
from utils import Validate_User_Input
from utils import setup
from utils import Download_Dataset
from classes import aux_code_thread


parser = argparse.ArgumentParser()

# Add valid arguments to take in
parser.add_argument('--download', '-dl', action='store_true',
                    help='This will Download the given subjects, session, tasks to the \'origin\' location.'
                         ' Note this will only work with the DMCC13 subject set')
parser.add_argument('--origin', '-o', help='set the origin of your data, your fmriprep output', required=True)
parser.add_argument('--subject', '-s', nargs='+', help='set the subject id to be processed', required=True)
parser.add_argument('--wave', '-w',
                    help='set the wave to be processed. expecting (wave1 wave2) WARNING: Can only process one wave at a time',
                    required=True)
parser.add_argument('--session', '-i', nargs='+',
                    help='The Sessions you would like to process these should be space seperated expecting (baseline proactive reactive)',
                    required=True)
parser.add_argument('--task', '-t', nargs='+',
                    help='The tasks you would like to process these should be space seperated expecting (Axcpt Cuedts Stern Stroop)',
                    required=True)
parser.add_argument('--destination', '-d', help='Where the output should be stored', required=True)
parser.add_argument('--volume', help='Run Volume Analysis', action='store_true')
parser.add_argument('--surface', help='Run Surface Analysis', action='store_true')
parser.add_argument('--preanalysis', help='Run PreAnalysis', action='store_true')
parser.add_argument('--analysis', help='Run Analysis', action='store_true')
parser.add_argument('--events', '-e', help='The event/onset files to be used in the glms', required=True)
parser.add_argument('--pipeline', '-p', help='The pipeline used to process the input images', required=True)
parser.add_argument('--ncpus', help='The Number of CPUs to use when processing the data', required=True)
parser.add_argument('--overwrite', help='if previous file was found overwrite the output', action='store_true')
parser.add_argument('--aux_analysis', help='A path that points to auxillerary analysis that will be ran after preanalysis and analysis')

##TODO Type in in argparse
args = parser.parse_args()

# Parse the Arguments Given
download = args.download
origin = args.origin
subjects = args.subject
wave = args.wave
tasks = args.task
sessions = args.session
destination = args.destination
events = args.events
run_volume = args.volume
run_surface = args.surface
run_preanalysis = args.preanalysis
run_analysis = args.analysis
pipeline = args.pipeline
ncpus = args.ncpus

aux_analysis = args.aux_analysis
overwrite = args.overwrite

globals.origin = origin
globals.subjects = subjects
globals.wave = wave
globals.tasks = tasks
globals.sessions = sessions
globals.destination = destination
globals.events = events
globals.run_volume = run_volume
globals.run_surface = run_surface
globals.run_analysis = run_analysis
globals.run_preanalysis = run_preanalysis
globals.pipeline = pipeline
globals.ncpus = ncpus
globals.aux_analysis = aux_analysis
globals.overwrite = overwrite

#Download Subjects from openneuro
if download:
    for subject in subjects:
        Download_Dataset.download_subject(subject, origin)

setup.setup_environment()
Validate_User_Input.validate_user_input(origin=origin, destination=destination, events=events, wave=wave,
                                        subjects=subjects, sessions=sessions, tasks=tasks, pipeline=pipeline,
                                        ncpus=ncpus, aux_analysis=aux_analysis)

pool = mp.Pool(int(ncpus))

for subject in subjects:
    # Create the output Folder
    if not os.path.exists(os.path.join(destination, subject)):  # If there is no subject folder in the destination create it
        os.mkdir(os.path.join(destination, subject))
    for session in sessions:
        for task in tasks:
            # Allow for asyncronous processing of the Data 4 tasks x 3 sessions means that each subject could utilize 12 cores
            pool.apply_async(Run_Analysis_Pipeline.analysis_pipeline, args=(origin, destination, events, wave, subject,
                                                                            session, task, pipeline, run_volume,
                                                                            run_surface, run_preanalysis, run_analysis))

pool.close()
pool.join()
pool = mp.Pool(int(ncpus))
YamlFileName = "Aux_Analysis.yaml"
if aux_analysis:
    Threads = aux_code_thread.build_threads_from_yaml(os.path.join(aux_analysis, YamlFileName))
    for Thread in Threads:
        print(f"Running Thread: {Thread.thread_name}")
        pool.apply_async(AuxAnalysis.aux_analysis, args=(Thread, aux_analysis))

pool.close()
pool.join()
