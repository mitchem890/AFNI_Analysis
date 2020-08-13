import os
import re
import sys

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
re_temp='(?:% s)' % '|'

def validate_pipeline(pipeline):
    valid_pipeline_format = ["hcp", "fmriprep"]
    temp = '(?:% s)' % '|'.join(valid_pipeline_format)
    if not re.match(temp, pipeline):
        print("Invalid pipeline input. Expecting either: fmriprep or hcp")
        raise OSError
    else:
        return True


def validate_origin(origin):
    if not os.path.exists(origin):
        print("origin: " + origin + " Does not exist")
        raise OSError
    else:
        return True


def validate_destination(destination):
    try:
        if not os.path.exists(destination):
            os.mkdir(destination)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Could not create destination")
        raise OSError


def validate_event_files(events):
    if not os.path.exists(events):
        print("events path: " + events + " Does not exist")
        raise OSError
    else:
        return True


def validate_subjects(subjects):
    valid_subject_format = ["[0-9][0-9][0-9][0-9][0-9][0-9]", "DMCC[0-9][0-9][0-9][0-9][0-9][0-9]"]
    temp = '(?:% s)' % '|'.join(valid_subject_format)
    try:
        for subject in subjects:
            if not re.match(temp, subject):
                raise OSError
    except OSError:
        print("One or more subjects have an invalid format. Expecting format: ###### or DMCC######")
        raise OSError

    return True


def validate_wave(wave):
    valid_wave_format = ["wave[1-9]"]
    temp = '(?:% s)' % '|'.join(valid_wave_format)
    try:
        if not re.match(temp, wave):
            raise OSError

    except OSError:
        print("Wave parameter does not match expected format: wave#")
        raise OSError

    return True


def validate_tasks(tasks):
    valid_tasks_format = ["Axcpt", "Cuedts", "Stern", "Stroop"]
    temp = '(?:% s)' % '|'.join(valid_tasks_format)
    try:
        for task in tasks:
            if not re.match(temp, task):
                raise OSError

    except OSError:
        print("Unknown task in task list expected: Axcpt Cuedts Stern or Stroop")
        raise OSError

    return True


def validate_sessions(sessions):
    valid_sessions_format = ["baseline", "proactive", "reactive"]
    temp = '(?:% s)' % '|'.join(valid_sessions_format)
    try:
        for session in sessions:
            if not re.match(temp, session):
                raise OSError

    except OSError:
        print("Unknown task in task list expected: baseline proactive reactive")
        raise OSError

    return True


def validate_ncpus(ncpus):
    try:
        int(ncpus)

    except ValueError:
        print("Invalid ncpus input. ncpus must be an integer type")
        raise ValueError

    return True


def validate_aux_analysis(aux_analysis):
    if aux_analysis is not None:
        try:
            if not os.path.exists(aux_analysis):
                raise OSError
        except OSError:
            print("aux_analysis path: " + aux_analysis + " Does not exist")
            raise OSError

    return True


def validate_user_input(origin, destination, events, pipeline, wave, subjects, tasks, sessions, ncpus, aux_analysis):
    validate_origin(origin)
    validate_destination(destination)
    validate_event_files(events)
    validate_pipeline(pipeline)
    validate_wave(wave)
    validate_subjects(subjects)
    validate_sessions(sessions)
    validate_tasks(tasks)
    validate_ncpus(ncpus)
    validate_aux_analysis(aux_analysis)
    ##TODO Raise single error at the end, return a tuple from each
