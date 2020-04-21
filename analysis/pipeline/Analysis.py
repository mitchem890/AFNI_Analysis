import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from classes import TaskGLMs
from utils import logger

#Run the volume 3ddeconvolve remlfit and roistats for each glm
def run_volume_glms(GLM_set):
    for glm in GLM_set.glms:

        print(f"Running {glm[0]}")
        if not os.path.exists(glm[0].output_dir):
            os.makedirs(glm[0].output_dir)

        os.chdir(glm[0].output_dir)
        glm[0].deconvolve.run_command()
        glm[0].remlfit.run_command()

        for roistats in glm[0].roistats:
            roistats.roistats.run_command()

#Run the volume 3ddeconvolve remlfit and roistats for each glm
def run_surface_glms(GLM_set):
    for glm in GLM_set.glms:
        print(f"Running {glm[1]}")
        if not os.path.exists(glm[1].output_dir):
            os.makedirs(glm[1].output_dir)

        os.chdir(glm[1].output_dir)
        glm[1].deconvolve.run_command()
        glm[1].remlfit.run_command()

        for roistats in glm[1].roistats:
            roistats.roistats.run_command()

        print(f"Running {glm[2]}")
        if not os.path.exists(glm[1].output_dir):
            os.makedirs(glm[1].output_dir)

        os.chdir(glm[1].output_dir)

        glm[2].deconvolve.run_command()
        glm[2].remlfit.run_command()

        for roistats in glm[2].roistats:
            roistats.roistats.run_command()


#Get the correct glm for the given session and task of the images This will return an object containing all of the glms and roistats
def get_GLMs(destination, images):
    if images[0].task == 'Axcpt':
        GLM_set = TaskGLMs.AxcptGLMs(working_dir=destination, images=images)
    elif images[0].task == 'Cuedts':
        GLM_set = TaskGLMs.CuedtsGLMs(working_dir=destination, images=images)
    elif images[0].task == 'Stern':
        GLM_set = TaskGLMs.SternGLMs(working_dir=destination, images=images)
    elif images[0].task == 'Stroop':
        GLM_set = TaskGLMs.StroopGLMs(working_dir=destination, images=images)
    return GLM_set

#This section kicks off the rest of the Functions
def analysis(destination, images, run_volume, run_surface):
    GLM_set=[]
    try:
        ##TODO Add the Preparcellated here
        GLM_set = get_GLMs(destination, images)

        if run_volume:
            run_volume_glms(GLM_set)
        if run_surface:
            run_surface_glms(GLM_set)
    except Exception as e:
        print(e)
        print("Error Running Analysis")
        logger.logger(e, 'error')
    return GLM_set