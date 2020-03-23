import logging
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from pipeline import Analysis, PreAnalysis
from classes import Images



def checkroistats(roistats):
    filename = os.path.join(roistats.working_dir, roistats.outfile)
    all_good = True
    if os.path.exists(filename):
        if os.stat(filename).st_size == 0:
            logging.info(f"WARNING: {filename} is empty!")
            all_good = False
    else:
        logging.info(f"WARNING: Could not find {filename}")
        all_good = False
    return all_good

def checkoutput(GLM_set):

    for glm in GLM_set.glms:

        #Check Volume
        for roistats in glm[0].roistats:
            volume_good = checkroistats(roistats)
        #Check Left Hem
        for roistats in glm[1].roistats:
            left_good = checkroistats(roistats)
        #Check right Hem
        for roistats in glm[2].roistats:
            right_good = checkroistats(roistats)
    all_good = volume_good and left_good and right_good
    return all_good


def checkinput(images):
    all_good = True
    if not len(images) == 2:
        logging.info(f"WARNING: Found {len(images)} images expected 2")
        all_good = False
    for image in images:
        logging.info(f"Found Image {image.file}")
    return all_good

def outputVerifier(images, GLM_set):
    try:
        logging.info(f"Verifiying input")
        input_good = checkinput(images)
    except:
        logging.info(f"Error while checking input images make sure they exist")
    try:
        logging.info(f"Verifiying output")
        output_good = checkoutput(GLM_set)
    except:
        logging.info(f"Error while checking output files make sure they exist")
    if input_good and output_good:
        logging.info(f"Both input and output look good")
    else:
        logging.info(f"There was an with either the input or the output")
