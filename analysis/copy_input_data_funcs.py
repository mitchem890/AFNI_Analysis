import os
import glob
from shutil import copyfile

def check_if_folders_exist(folders):
    for folder in folders:
        if not os.path.isdir(folder):
            print('ERROR: folder ' + str(folder) + ' does not exist. Please check.')
            exit()


def check_evts(event_dir):
    print('Checking evts for blanks')
    files = os.listdir(event_dir)
    for file in files:
        for line in file:
            if len(line.strip().strip('*')) == 0:
                print('found empty line in file ' + str(file))


def copy_evts(evts_dir, out_dir, task, session):
    files = glob.glob(os.path.join(evts_dir,subject+'_' +task+'_'+session+'_*'))
    for file in files:
        copyfile(file, out_dir)




def resample_niftis(niftis):





