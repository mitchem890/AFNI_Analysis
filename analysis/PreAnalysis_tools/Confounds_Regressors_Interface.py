import csv
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import pandas as pd
from classes import BashCommand


# Pull the movement regressors out of fmriprep tsv for use with the fmriprep output
def get_movement_regressors(input, output):
    motion = pd.read_csv(input, delimiter='\t', encoding='utf-8')

    data = {'trans_x': motion['trans_x'], 'trans_y': motion['trans_y'], 'trans_z': motion['trans_z'],
            'rot_x': motion['rot_x'], 'rot_y': motion['rot_y'], 'rot_z': motion['rot_z']}
    df = pd.DataFrame(data=data)
    df = df[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
    df.to_csv(output, sep='\t', header=False, index=False, quoting=csv.QUOTE_NONE, float_format='%.8f')


# Pull the FD out of fmriprep tsv for use with the fmriprep output
def get_fd(input, output):
    motion = pd.read_csv(input, delimiter='\t', encoding='utf-8')
    data = {'framewise_displacement': motion['framewise_displacement']}
    df = pd.DataFrame(data=data)
    df.iloc[0] = 0
    df.round(5)
    df.to_csv(output, sep='\t', header=False, index=False, quoting=csv.QUOTE_NONE, float_format='%.8f')


# Pull the DVARS out of fmriprep tsv for use with the fmriprep output
def get_dvars(input, output):
    motion = pd.read_csv(input, delimiter='\t', encoding='utf-8')
    data = {'std_dvars': motion['std_dvars']}
    df = pd.DataFrame(data=data)
    df.iloc[0] = 0
    df.round(5)
    df.to_csv(output, sep='\t', index=False, header=False, quoting=csv.QUOTE_NONE, float_format='%.8f')


# Create the FD mask with a threshold of .9 for use with the fmriprep output
def make_fd_mask(input, output):
    data = BashCommand.MakeFDMask(infile=input).run_command()
    with open(output, 'w') as f:
        for i in data:
            f.write(i + '\n')
