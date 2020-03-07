import os
import re


# origin = args.origin
# subjects = args.subject
# wave = args.wave
# tasks = args.task
# sessions = args.session
# destination = args.destination
# events = args.events
# run_volume = args.volume
# run_surface = args.surface
# run_preanalysis = args.preanalysis
# run_analysis = args.analysis
# pipeline = args.pipeline


def validate_pipeline(pipeline):
    valid_pipeline_format = ["hcp", "fmriprep"]
    temp = '(?:% s)' % '|'.join(valid_pipeline_format)
    try:
        if not re.match(temp, pipeline):
            raise IOError

    except IOError:
        print("Invalid pipeline input. Expecting either: fmriprep or hcp")


def validate_origin(origin):
    try:
        if not os.path.exists(origin):
            raise IOError
    except IOError:
        print("origin: " + origin + " Does not exist")


def validate_destination(destination):
    try:
        if not os.path.exists(destination):
            os.mkdir(destination)
    except IOError:
        print("Could not create destination")


def validate_event_files(events):
    try:
        if not os.path.exists(events):
            raise IOError
    except IOError:
        print("events path: " + events + " Does not exist")
        ##TODO sys.exit(error#) Check argparse for validation Function


def validate_subjects(subjects):
    valid_subject_format = ["[0-9][0-9][0-9][0-9][0-9][0-9]", "DMCC[0-9][0-9][0-9][0-9][0-9][0-9]"]
    temp = '(?:% s)' % '|'.join(valid_subject_format)
    try:
        for subject in subjects:
            if not re.match(temp, subject):
                raise IOError

    except IOError:
        print("One or more subjects have an invalid format. Expecting format: ###### or DMCC######")


def validate_wave(wave):
    valid_wave_format = ["wave[1-9]"]
    temp = '(?:% s)' % '|'.join(valid_wave_format)
    try:
        if not re.match(temp, wave):
            raise IOError

    except IOError:
        print("Wave parameter does not match expected format: wave#")


def validate_tasks(tasks):
    valid_tasks_format = ["Axcpt", "Cuedts", "Stern", "Stroop"]
    temp = '(?:% s)' % '|'.join(valid_tasks_format)
    try:
        for task in tasks:
            if not re.match(temp, task):
                raise IOError

    except IOError:
        print("Unknown task in task list expected: Axcpt Cuedts Stern or Stroop")


def validate_sessions(sessions):
    valid_sessions_format = ["baseline", "proactive", "reactive"]
    temp = '(?:% s)' % '|'.join(valid_sessions_format)
    try:
        for session in sessions:
            if not re.match(temp, session):
                raise IOError

    except IOError:
        print("Unknown task in task list expected: baseline proactive reactive")


def validate_ncpus(ncpus):
    try:
        int(ncpus)

    except IOError:
        print("Invalid ncpus input. ncpus must be an integer type")


def validate_user_input(origin, destination, events, pipeline, wave, subjects, tasks, sessions, ncpus):
    validate_origin(origin)
    validate_destination(destination)
    validate_event_files(events)
    validate_pipeline(pipeline)
    validate_wave(wave)
    validate_subjects(subjects)
    validate_sessions(sessions)
    validate_tasks(tasks)
    validate_ncpus(ncpus)
    ##TODO Raise single error at the end, return a tuple from each
