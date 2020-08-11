import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from utils import logger
from pipeline import Analysis, PreAnalysis
from classes import Images



def checkroistats(roistats):
    filename = os.path.join(roistats.working_dir, roistats.outfile)
    all_good = True
    if os.path.exists(filename):
        if os.stat(filename).st_size == 0:
            logger.logger(f"WARNING: {filename} is empty!", 'warning')
            all_good = False
    else:
        logger.logger(f"WARNING: Could not find {filename}", 'warning')
        all_good = False
    return all_good

def checkoutput(GLM_set):

    for glm in GLM_set.glms:

        #Check Volume
        for roistats in glm[0].Roistats:
            volume_good = checkroistats(roistats)
        #Check Left Hem
        for roistats in glm[1].Roistats:
            left_good = checkroistats(roistats)
        #Check right Hem
        for roistats in glm[2].Roistats:
            right_good = checkroistats(roistats)
    all_good = volume_good and left_good and right_good
    return all_good


def checkinput(images):
    all_good = True
    if not len(images) == 2:
        logger.logger(f"WARNING: Found {len(images)} images expected 2", 'warning')
        all_good = False
    for image in images:
        logger.logger(f"Found Image {image.file}", 'warning')
    return all_good

def outputVerifier(images, GLM_set):
    try:
        logger.logger(f"Verifiying input", 'info')
        input_good = checkinput(images)
    except:
        logger.logger(f"Error while checking input images make sure they exist", 'error')
    try:
        logger.logger(f"Verifiying output", 'info')
        output_good = checkoutput(GLM_set)
    except:
        logger.logger(f"Error while checking output files make sure they exist", 'error')
    if input_good and output_good:
        logger.logger(f"Both input and output look good", 'info')
    else:
        logger.logger(f"There was an with either the input or the output", 'error')
