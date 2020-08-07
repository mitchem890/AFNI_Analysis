#This will split files into one run for each file
import glob
import os

def split_evt(filename, outfile, line_number):
    print(f"Splitting evt {filename} at line number {line_number}")
    f = open(filename, "r")
    w = open(outfile, "a")
    w.write(f.readlines()[int(line_number)])
    f.close()
    f.close()

def split_tr_lengthed_files(filename, outfile, run_length, line_start):
    f = open(filename, "r")
    w = open(outfile, "a")
    all_lines = f.readlines()
    line_end_idx = run_length + line_start

    lines = all_lines[line_start:line_end_idx]
    for line in lines:
        w.write(line)
    f.close()
    w.close()

def find_and_split_evts(dir, images):
    print("Running EVT splitter")
    prefix=f"{images[0].subject}_{images[0].task}_{images[0].session}_"
    for file in list(set(glob.glob(os.path.join(dir, f"{prefix}*.txt"))) - set(glob.glob((os.path.join(dir, f"{prefix}*run[0-9].txt"))))):
        for image in images:
            outfile = f"{file.rsplit('.txt')[0]}_run{image.run_num}.txt"
            split_evt(file, outfile, int(image.run_num)-1)

def find_and_split_movement(dir, images):
    first_tr_of_run = 0
    print("Running movement splitter")
    for image in images:
        print(image)
        filename = os.path.join(dir, f"movregs_FD_mask.txt")
        outfile = os.path.join(dir, f"movregs_FD_mask_run{image.run_num}.txt")
        split_tr_lengthed_files(filename=filename, outfile=outfile,
                                run_length=image.run_length, line_start=first_tr_of_run)
        filename = os.path.join(dir, f"motion_demean_{image.session}.1D")
        outfile = os.path.join(dir, f"motion_demean_{image.session}_run{image.run_num}.1D")
        split_tr_lengthed_files(filename=filename, outfile=outfile,
                                run_length=int(image.run_length), line_start=first_tr_of_run)
        first_tr_of_run = image.run_length + first_tr_of_run