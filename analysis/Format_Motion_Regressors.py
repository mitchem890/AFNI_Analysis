import os
import pandas as pd
import csv



#append files together this is used because run1 and run2 are processed through afni at the same time
#supply a list of files and an out file name
def append(filelist, outfile):

    if os.path.exists(outfile):
        os.remove(outfile)

    for file in filelist:

        fin = open(file, "r")
        data = fin.read()
        fin.close()

        fout = open(outfile, "a")
        fout.write(data)
        fout.close()

#format the motion regressors so that we can run afni, basically append the 2 runs of movment regressors and FDs and DVARs together
def format_motion_regressors(path, subject, session, task):

        print("Format Motion regressors")
        fullpath=os.path.join(path, subject,'INPUT_DATA', task, session)
        #List of motion regressors
        #TODO check for correct run Number
        move_regs=[os.path.join(fullpath, 'Movement_Regressors_' + task + session[0:3].title() + '1_AP.txt'),
                   os.path.join(fullpath, 'Movement_Regressors_' + task + session[0:3].title() + '2_PA.txt')]
        #outfilename for the motion regressors
        mov_regs_out=os.path.join(fullpath, "movregs12.txt")
        #append the two motion regressors together and store them in the outfile
        append(move_regs, mov_regs_out)

        #List of framewise Displacement files
        mov_regs_FD=[os.path.join(fullpath, subject + '_tfMRI_' + task + session[0:3].title() + '1_AP_FD.txt'),
                     os.path.join(fullpath, subject + '_tfMRI_' + task + session[0:3].title() + '2_PA_FD.txt')]
        #the Framewise Displacement outfile
        mov_regs_FD_out = os.path.join(fullpath, 'movregs_FD.txt')
        #append the outfiles together
        append(mov_regs_FD, mov_regs_FD_out)

        #A list of the Framewise Displacement Mask
        mov_regs_FD_masks=[os.path.join(fullpath, subject + '_tfMRI_'+ task + session[0:3].title() + '1_AP_FD_mask.txt'),
                           os.path.join(fullpath, subject + '_tfMRI_' + task + session[0:3].title() + '2_PA_FD_mask.txt')]
        #The outfile for the Framewise displacement mask
        mov_regs_FD_masks_out=os.path.join(fullpath, "movregs_FD_mask.txt")
        #append the files together
        append(mov_regs_FD_masks, mov_regs_FD_masks_out)

        #We just want the first 6 movement regressors not their derivatives
        mov_regs_six_out=os.path.join(fullpath, "movregs6.txt")

        #TODO maybe write in a seperate func
        #read in the 12 column movement regressors csv
        motion = pd.read_csv(mov_regs_out, delimiter='\t', encoding='utf-8')

        #Just get the first 6 movement regressors
        data = motion.iloc[:, 0:6]
        #put them into a dataframe
        df = pd.DataFrame(data=data)
        #print them out to a csv
        df.to_csv(mov_regs_six_out, sep='\t', index=False, quoting=csv.QUOTE_NONE)

#        print("Could not format motion regressors: " + 'Movement_Regressors_' + task + session[0:3].title())