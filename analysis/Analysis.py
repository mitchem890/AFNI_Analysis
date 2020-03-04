import os

import RunShellFunc as rs
from classes import TaskGLMs


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


# This Section Includes all the GLMs and roistats
def analysis(destination, images, run_volume, run_surface):

    if images[0].task == 'Axcpt':
        GLM_set = TaskGLMs.AxcptGLMs(working_dir=destination,images=images)
    elif images[0].task == 'Cuedts':
        GLM_set = TaskGLMs.CuedtsGLMs(working_dir=destination,images=images)
    elif images[0].task == 'Stern':
        GLM_set = TaskGLMs.SternGLMs(working_dir=destination,images=images)
    elif images[0].task == 'Stroop':
        GLM_set = TaskGLMs.StroopGLMs(working_dir=destination,images=images)

    if run_volume:
        run_volume_glms(GLM_set)
    if run_surface:
        run_surface_glms(GLM_set)
