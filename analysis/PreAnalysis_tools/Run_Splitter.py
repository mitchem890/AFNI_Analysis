#This will split files into one run for each file
import glob
import os

def split_evt(filename, outfile, line_number):
    f = open(filename, "r")
    w = open(outfile, "a")
    w.write(f.readlines()[int(line_number)])

def split_tr_lengthed_files(filename, outfile, run_length, line_start):
    f = open(filename, "r")
    w = open(outfile, "a")
    line_end = int(run_length) + int(line_start)
    w.write(f.readlines()[line_start:line_end])


def find_and_split_evts(dir, images):
    for image in images:
        for file in glob.glob(os.path.join(dir, f"{image.subject}_{image.task}_{image.session}_*txt")):
            outfile=f"{file.rsplit('.txt')[0]}_{image.run_num}.txt"
            split_evt(file, outfile, image.run_num)

def find_and_split_movement(dir, images):
    first_tr_of_run = 0
    for image in images:
        filename = os.path.join(dir, f"movregs_FD_mask.txt")
        outfile = os.path.join(dir, f"movregs_FD_mask_{image.run_num}.txt")
        split_tr_lengthed_files(filename=filename, outfile=outfile,
                                run_length=int(image.tr), line_start=int(first_tr_of_run))
        filename = os.path.join(dir, f"motion_demean_{image.session}.1D")
        outfile = os.path.join(dir, f"motion_demean_{image.session}_{image.run_num}.1D")
        split_tr_lengthed_files(filename=filename, outfile=outfile,
                                run_length=int(image.tr), line_start=int(first_tr_of_run))
        first_tr_of_run = int(image.tr) + first_tr_of_run