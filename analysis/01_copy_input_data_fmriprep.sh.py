import os
import copy_input_data_funcs as cidf
import ConfigReader as cr
import logging
import argparse
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('--Subjects', '-s', help='subject ID. Use double quotes for a list of subjects')
parser.add_argument('--Tasks', '-t', help='Task name. Use double quotes for a list  (mandatory)')
parser.add_argument('--Sessions', '-i', help='Session name. Use double quotes for a list  (mandatory)')
parser.add_argument('--Origin', '-o', help='Path to dir containing input subject folder (mandatory)')
parser.add_argument('--Destination', '-d', help='Path to dir containing output subject folder (mandatory)')
parser.add_argument('--Events', '-e', help='Path to dir containing onset times (mandatory)')
args = parser.parse_args()

subjects = args.Subjects
tasks = args.Tasks
session = args.Sessions
origin = args.Origin
destination = args.Destination
event = args.Events


for subject in subjects:

    in_dir = os.path.join(origin, 'sub-' + subject)
    evts_dir = os.path.join(event, subject, 'evts')
    folders = []

    folders.append(in_dir)
    folders.append(destination)
    folders.append(events)

    cidf.check_if_folders_exist(folders)

    for task in tasks:
        for session in sessions:

            out_dir = os.path.join(destination, 'sub-' + subject, 'INPUT_DATA', task, session)

            check_evts(evts_dir)
            copy_evts(evts_dir, out_dir, task, session)
            resample_niftis(nifti_name, mask)
            get_fsaverage(in_dir, session, task)
            get_confounds(in_dir, session, task)
            get_FD(in_dir, session, task)
            get_six_axis(in_dir, session, task)
            create_mask()
            get_stdDVARS()
            copy_evts()

