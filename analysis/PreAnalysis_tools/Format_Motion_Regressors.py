import csv
import os
import pandas as pd
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from classes import Images


# append files together this is used because run1 and run2 are processed through afni at the same time
# supply a list of files and an out file name
def append(filelist, outfile):
    if os.path.exists(outfile):
        os.remove(outfile)

    for file in filelist:  ##TODO Fix This file

        fin = open(file, "r")
        data = fin.read()
        fin.close()

        fout = open(outfile, "a")
        fout.write(data)
        fout.close()


# format the motion regressors so that we can run afni, basically append the 2 runs of movment regressors and FDs and DVARs together
def format_motion_regressors(path, images: Images.preprocessed_image):
    print(f"Formatting Motion regressors: {images[0]} and {images[1].encoding}")
    fullpath = os.path.join(path, images[0].subject, 'INPUT_DATA', images[0].task, images[0].session)
    # List of motion regressors
    root_names = []

    move_regs = [os.path.join(fullpath, f"Movement_Regressors_{images[0].root_name}.txt"),
                 os.path.join(fullpath, f"Movement_Regressors_{images[1].root_name}.txt")]
    # outfilename for the motion regressors
    mov_regs_out = os.path.join(fullpath, "movregs12.txt")

    # append the two motion regressors together and store them in the outfile
    append(move_regs, mov_regs_out)

    # List of framewise Displacement files
    mov_regs_FD = [os.path.join(fullpath, f"{images[0].subject}_tfMRI_{images[0].root_name}_FD.txt"),
                   os.path.join(fullpath, f"{images[1].subject}_tfMRI_{images[1].root_name}_FD.txt")]
    # the Framewise Displacement outfile
    mov_regs_FD_out = os.path.join(fullpath, 'movregs_FD.txt')
    # append the outfiles together
    append(mov_regs_FD, mov_regs_FD_out)

    # A list of the Framewise Displacement Mask
    mov_regs_FD_masks = [os.path.join(fullpath, f"{images[0].subject}_tfMRI_{images[0].root_name}_FD_mask.txt"),
                         os.path.join(fullpath, f"{images[1].subject}_tfMRI_{images[1].root_name}_FD_mask.txt")]
    # The outfile for the Framewise displacement mask
    mov_regs_FD_masks_out = os.path.join(fullpath, "movregs_FD_mask.txt")
    # append the files together
    append(mov_regs_FD_masks, mov_regs_FD_masks_out)

    # We just want the first 6 movement regressors not their derivatives
    mov_regs_six_out = os.path.join(fullpath, "movregs6.txt")

    # TODO maybe write in a seperate func
    # read in the 12 column movement regressors csv

    motion = pd.read_csv(mov_regs_out, header=None, delimiter='\t', encoding='utf-8')

    # Just get the first 6 movement regressors
    data = motion.iloc[:, 0:6]
    # put them into a dataframe
    df = pd.DataFrame(data=data)
    # print them out to a csv
    df.to_csv(mov_regs_six_out, sep='\t', index=False, header=None, quoting=csv.QUOTE_NONE, float_format='%.8f')
