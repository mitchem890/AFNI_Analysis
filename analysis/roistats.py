import os
import ConfigGLMs
import RunShellFunc as rs

def block_roistats(subject, task, session, mb, data_dir, censor):
    print("Running Volume Block Roistats: " + subject + " " + session + " " + task)
    conditions=["ON"]
    design="BLOCKS"

    # ----- atlases
    atlases_dir = ConfigGLMs.Atlas_Dir

    if mb == "4":
        atlases =ConfigGLMs.VolumeAtlasesMB4
    elif mb == "8":
        atlases =ConfigGLMs.VolumeAtlasesMB8


    work_dir=os.path.join(data_dir,subject,'RESULTS',task)

    for condition in conditions:
        glm=session+"_"+condition+"_"+design
        name=condition+"_"+design

        if censor:
            glm=glm+"_censored"


    stats_file=os.path.join(work_dir,glm,'STATS_'+subject+'_REML.nii.gz')

    if not os.path.exists(stats_file):

        print("WARNING: "+stats_file+" doesn't exist. Check if this is correct.")

    else:

        for atlas in atlases:
            rs.run_shell_command("bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                                " -n " + name + " -w " + os.path.join(work_dir, glm) +
                                " -a " + os.path.join(atlases_dir, atlas) +
                                " -e " + session +
                                " -s " + subject +
                                " -r \".nii.gz\" -o \"_blocks\"")



def contrast_roistats(subject, task, session, mb, data_dir, censor):
    print("Running Volume Contrast Roistats: " + subject + " " + session + " " + task)

    work_dir = os.path.join(data_dir, subject, 'RESULTS', task)

    design = "EVENTS"

    # ----- atlases
    atlases_dir = ConfigGLMs.Atlas_Dir

    if mb == "4":
        atlases =ConfigGLMs.VolumeAtlasesMB4
    elif mb == "8":
        atlases =ConfigGLMs.VolumeAtlasesMB8



    if task == "Axcpt":
        glm_id = ConfigGLMs.AxcptEventContrastsGLMids
        contrasts = ConfigGLMs.AxcptEventContrastLabels
        num_contrasts =len(contrasts) # number of glms per task

    elif task == "Cuedts":
        glm_id = ConfigGLMs.CuedtsEventContrastsGLMids
        contrasts = ConfigGLMs.CuedtsEventContrastLabels
        num_contrasts =len(contrasts) # contrasts[@]} # number of glms per task

    elif task == "Stern":
        glm_id = ConfigGLMs.SternEventContrastsGLMids
        contrasts = ConfigGLMs.SternEventContrastLabels
        num_contrasts = len(contrasts) # contrasts[@]} # number of glms per task

    elif task == "Stroop":
        glm_id = ConfigGLMs.StroopEventContrastsGLMids
        contrasts = ConfigGLMs.StroopEventContrastLabels
        num_contrasts =len(contrasts) # number of glms per task
    else:
        "ERROR: no task named ${task}"



    for i in range(0, num_contrasts):

        contrast=contrasts[i]

        glm=session+"_"+glm_id[i]+"_"+design

        if censor == True:
            glm=glm+"_censored"


        stats_file=os.path.join(work_dir,glm,"STATS_"+subject+"_REML.nii.gz")

        if not os.path.exists(stats_file):
            print("WARNING: "+stats_file+ "doesn't exist. Check if this is correct.")
        else:

            for atlas in atlases:
                rs.run_shell_command(
                    "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                    " -n " + contrast + " -w " + os.path.join(work_dir, glm) +
                    " -a " + os.path.join(atlases_dir, atlas) +
                    " -e " + session +
                    " -s " + subject +
                    " -r \".nii.gz\" -o \"_tents\"")


def mixed_roistats(subject, task, session, mb, data_dir, censor):
    print("Running Volume Mixed Roistats: " + subject + " " + session + " " + task)

    design = "MIXED"
    conditions = ["ON"]

    # ----- atlases
    atlases_dir =ConfigGLMs.Atlas_Dir

    if mb == "4":
        atlases =ConfigGLMs.VolumeAtlasesMB4
    elif mb == "8":
        atlases =ConfigGLMs.VolumeAtlasesMB8
    else:
        print("ERROR :\tNo MB factor of " + mb)


    work_dir = os.path.join(data_dir, subject, 'RESULTS', task)

    for condition in conditions:

            glm = session+"_"+condition+"_"+design
            if censor == True:
                glm = glm+"_censored"

            stats_file = os.path.join(work_dir, glm, "STATS_" + subject + "_REML.nii.gz")
            if not os.path.exists(stats_file):
                print("\nWARNING: "+stats_file+" doesn't exist. Check if this is correct.")
            else:


                name=condition+"_BLOCKS"

                for atlas in atlases:

                    name = condition + "_BLOCKS"

                    rs.run_shell_command(
                        "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                        " -n " + name + " -w " + os.path.join(work_dir, glm) +
                        " -a " + os.path.join(atlases_dir, atlas) +
                        " -e " + session +
                        " -s " + subject +
                        " -r \".nii.gz\" -o \"_blocks\"")


                    name = condition + "_blockONandOFF"

                    rs.run_shell_command(
                        "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                        " -n " + name + " -w " + os.path.join(work_dir, glm) +
                        " -a " + os.path.join(atlases_dir, atlas) +
                        " -e " + session +
                        " -s " + subject +
                        " -r \".nii.gz\" -o \"_tents\"")


                    name = condition + "_trials"

                    rs.run_shell_command(
                    "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                    " -n " + name + " -w " + os.path.join(work_dir, glm) +
                    " -a " + os.path.join(atlases_dir, atlas) +
                    " -e " + session +
                    " -s " + subject +
                    " -r \".nii.gz\" -o \"_tents\"")


def single_regressors_roistats(subject, task, session, mb, data_dir, censor):
    print("Running Volume Single Regressor Roistats: " + subject + " " + session + " " + task)

    design = "EVENTS"

    # ----- atlases
    atlases_dir =ConfigGLMs.Atlas_Dir

    if mb == "4":
        atlases =ConfigGLMs.VolumeAtlasesMB4
    elif mb == "8":
        atlases =ConfigGLMs.VolumeAtlasesMB8
    else:
        print("ERROR :\tNo MB factor of " + mb)

    work_dir = os.path.join(data_dir, subject, 'RESULTS', task)

    if task == "Axcpt":
        conditions = ConfigGLMs.AxcptSingleRegressorConditions
        glm_id = ConfigGLMs.AxcptSingleRegressorGLMids
        num_conditions =len(glm_id)

    elif task == "Cuedts":
        conditions = ConfigGLMs.CuedtsSingleRegressorConditions
        glm_id = ConfigGLMs.CuedtsSingleRegressorGLMids
        num_conditions =len(glm_id)

    elif task == "Stern":
        conditions = ConfigGLMs.SternSingleRegressorConditions
        glm_id = ConfigGLMs.SternSingleRegressorGLMids
        num_conditions = len(glm_id)
    elif task == "Stroop":
        conditions = ConfigGLMs.SternSingleRegressorConditions
        glm_id = ConfigGLMs.SternSingleRegressorGLMids
        num_conditions = len(glm_id)

    if task == "Stroop" and session.lower() == "reactive":
        conditions = ConfigGLMs.StroopSingleRegressorConditions
        glm_id = ConfigGLMs.SternSingleRegressorGLMids
        num_conditions = len(glm_id)


    for i in range(0, num_conditions):
        condition =conditions[i]

        glm = session+"_"+glm_id[i]+"_"+design

        if censor == True:
            glm = glm+"_censored"

        stats_file = os.path.join(work_dir, glm, "STATS_" + subject + "_REML.nii.gz")

        if not os.path.exists(stats_file):
            print("WARNING: "+stats_file+"doesn't exist. Check if this is correct.")
        else:

            for atlas in atlases:
                # roistats
                name = condition

                rs.run_shell_command(
                    "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                    " -n " + name + " -w " + os.path.join(work_dir, glm) +
                    " -a " + os.path.join(atlases_dir, atlas) +
                    " -e " + session +
                    " -s " + subject +
                    " -r \".nii.gz\" -o \"_tents\"")


def block_roistats_Surface(subject, task, session, mb, hemisphere, data_dir, censor, fsaverage5=False):
    print("Running Surface Block Roistats: " + subject + " " + session + " " + task)
    conditions=["ON"]
    design="BLOCKS"

    # ----- atlases
    atlases_dir = ConfigGLMs.Atlas_Dir

    if mb == "4":
        atlases =ConfigGLMs.SurfaceAtlasesMB4
    elif mb == "8":
        atlases =ConfigGLMs.SurfaceAtlasesMB8

    if fsaverage5:
        atlases=ConfigGLMs.SurfaceAtlasesFS5


    work_dir=os.path.join(data_dir,subject,'SURFACE_RESULTS',task)

    for condition in conditions:
        glm = session+"_"+condition+"_"+design
        name = condition+"_"+design

        if censor:
            glm=glm+"_censored"


    stats_file=os.path.join(work_dir,glm,'STATS_'+subject+'_REML_' + hemisphere + '.func.gii')

    if not os.path.exists(stats_file):

        print("WARNING: "+stats_file+" doesn't exist. Check if this is correct.")

    else:

        for atlas in atlases:
            if atlas == "gordon_333":
                extension="_"+hemisphere+".func.gii"
            else:
                extension="_"+hemisphere+".label.gii"
            rs.run_shell_command("bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                                " -n " + name + " -w " + os.path.join(work_dir, glm) +
                                " -a " + os.path.join(atlases_dir, atlas) +
                                " -e " + session +
                                " -s " + subject +
                                " -r \""+extension+"\" -o \"_blocks\"")



def contrast_roistats_Surface(subject, task, session, mb, hemisphere, data_dir, censor, fsaverage5=False):
    print("Running Surface Contrast Roistats: " + subject + " " + session + " " + task)

    work_dir = os.path.join(data_dir, subject, 'SURFACE_RESULTS', task)

    design = "EVENTS"

    # ----- atlases
    atlases_dir = ConfigGLMs.Atlas_Dir

    if mb == "4":
        atlases =ConfigGLMs.VolumeAtlasesMB4
    elif mb == "8":
        atlases =ConfigGLMs.VolumeAtlasesMB8

    if fsaverage5:
        atlases=ConfigGLMs.SurfaceAtlasesFS5



    if task == "Axcpt":
        glm_id = ConfigGLMs.AxcptEventContrastsGLMids
        contrasts = ConfigGLMs.AxcptEventContrastLabels
        num_contrasts =len(contrasts) # number of glms per task

    elif task == "Cuedts":
        glm_id = ConfigGLMs.CuedtsEventContrastsGLMids
        contrasts = ConfigGLMs.CuedtsEventContrastLabels
        num_contrasts =len(contrasts) # contrasts[@]} # number of glms per task

    elif task == "Stern":
        glm_id = ConfigGLMs.SternEventContrastsGLMids
        contrasts = ConfigGLMs.SternEventContrastLabels
        num_contrasts = len(contrasts) # contrasts[@]} # number of glms per task

    elif task == "Stroop":
        glm_id = ConfigGLMs.StroopEventContrastsGLMids
        contrasts = ConfigGLMs.StroopEventContrastLabels
        num_contrasts =len(contrasts) # number of glms per task
    else:
        "ERROR: no task named ${task}"



    for i in range(0, num_contrasts):

        contrast=contrasts[i]

        glm=session+"_"+glm_id[i]+"_"+design

        if censor == True:
            glm=glm+"_censored"


        stats_file=os.path.join(work_dir,glm,'STATS_'+subject+'_REML_' + hemisphere + '.func.gii')

        if not os.path.exists(stats_file):
            print("WARNING: "+stats_file+ "doesn't exist. Check if this is correct.")
        else:

            for atlas in atlases:
                if atlas == "gordon_333":
                    extension = "_" + hemisphere + ".func.gii"
                else:
                    extension = "_" + hemisphere + ".label.gii"

                rs.run_shell_command(
                    "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                    " -n " + contrast + " -w " + os.path.join(work_dir, glm) +
                    " -a " + os.path.join(atlases_dir, atlas) +
                    " -e " + session +
                    " -s " + subject +
                    " -r \""+extension+"\" -o \"_tents\"")


def mixed_roistats_Surface(subject, task, session, mb, hemisphere, data_dir, censor, fsaverage5=False):
    print("Running Surface Mixed Roistats: " + subject + " " + session + " " + task)

    design = "MIXED"
    conditions = ["ON"]

    # ----- atlases
    atlases_dir =ConfigGLMs.Atlas_Dir

    if mb == "4":
        atlases =ConfigGLMs.VolumeAtlasesMB4
    elif mb == "8":
        atlases =ConfigGLMs.VolumeAtlasesMB8
    else:
        print("ERROR :\tNo MB factor of " + mb)

    if fsaverage5:
        atlases=ConfigGLMs.SurfaceAtlasesFS5


    work_dir = os.path.join(data_dir, subject, "SURFACE_RESULTS", task)

    for condition in conditions:

            glm = session+"_"+condition+"_"+design
            if censor == True:
                glm = glm+"_censored"

            stats_file = os.path.join(work_dir,glm,'STATS_'+subject+'_REML_' + hemisphere + '.func.gii')
            if not os.path.exists(stats_file):
                print("\nWARNING: "+stats_file+" doesn't exist. Check if this is correct.")
            else:


                name=condition+"_BLOCKS"

                for atlas in atlases:
                    if atlas == "gordon_333":
                        extension = "_" + hemisphere + ".func.gii"
                    else:
                        extension = "_" + hemisphere + ".label.gii"

                    name = condition + "_BLOCKS"

                    rs.run_shell_command(
                        "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                        " -n " + name + " -w " + os.path.join(work_dir, glm) +
                        " -a " + os.path.join(atlases_dir, atlas) +
                        " -e " + session +
                        " -s " + subject +
                        " -r \""+extension+"\" -o \"_blocks\"")


                    name = condition + "_blockONandOFF"

                    rs.run_shell_command(
                        "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                        " -n " + name + " -w " + os.path.join(work_dir, glm) +
                        " -a " + os.path.join(atlases_dir, atlas) +
                        " -e " + session +
                        " -s " + subject +
                        " -r \""+extension+"\" -o \"_tents\"")


                    name = condition + "_trials"

                    rs.run_shell_command(
                    "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                    " -n " + name + " -w " + os.path.join(work_dir, glm) +
                    " -a " + os.path.join(atlases_dir, atlas) +
                    " -e " + session +
                    " -s " + subject +
                    " -r \""+extension+"\" -o \"_tents\"")


def single_regressors_roistats_Surface(subject, task, session, mb, hemisphere, data_dir, censor, fsaverage5=False):
    print("Running Surface Single Regressors Roistats: " + subject + " " + session + " " + task)

    design = "EVENTS"

    # ----- atlases
    atlases_dir =ConfigGLMs.Atlas_Dir

    if mb == "4":
        atlases =ConfigGLMs.VolumeAtlasesMB4
    elif mb == "8":
        atlases =ConfigGLMs.VolumeAtlasesMB8
    else:
        print("ERROR :\tNo MB factor of " + mb)

    if fsaverage5:
        atlases=ConfigGLMs.SurfaceAtlasesFS5

    work_dir = os.path.join(data_dir, subject, "SURFACE_RESULTS", task)

    if task == "Axcpt":
        conditions = ConfigGLMs.AxcptSingleRegressorConditions
        glm_id = ConfigGLMs.AxcptSingleRegressorGLMids
        num_conditions =len(glm_id)

    elif task == "Cuedts":
        conditions = ConfigGLMs.CuedtsSingleRegressorConditions
        glm_id = ConfigGLMs.CuedtsSingleRegressorGLMids
        num_conditions =len(glm_id)

    elif task == "Stern":
        conditions = ConfigGLMs.SternSingleRegressorConditions
        glm_id = ConfigGLMs.SternSingleRegressorGLMids
        num_conditions = len(glm_id)
    elif task == "Stroop":
        conditions = ConfigGLMs.StroopSingleRegressorConditions
        glm_id = ConfigGLMs.StroopSingleRegressorGLMids
        num_conditions = len(glm_id)

    if task == "Stroop" and session.lower() == "reactive":
        conditions = ConfigGLMs.StroopReaSingleRegressorConditions
        glm_id = ConfigGLMs.StroopReaSingleRegressorGLMids
        num_conditions = len(glm_id)


    for i in range(0, num_conditions):
        condition =conditions[i]

        glm = session+"_"+glm_id[i]+"_"+design

        if censor == True:
            glm = glm+"_censored"

        stats_file = os.path.join(work_dir,glm,'STATS_'+subject+'_REML_' + hemisphere + '.func.gii')

        if not os.path.exists(stats_file):
            print("WARNING: "+stats_file+"doesn't exist. Check if this is correct.")
        else:

            for atlas in atlases:
                # roistats
                if atlas == "gordon_333":
                    extension = "_" + hemisphere + ".func.gii"
                else:
                    extension = "_" + hemisphere + ".label.gii"

                name = condition

                rs.run_shell_command(
                    "bash /home/mitchell/dockerprojects/AfniAnalysis/analysis/Roistats.sh -i " + stats_file +
                    " -n " + name + " -w " + os.path.join(work_dir, glm) +
                    " -a " + os.path.join(atlases_dir, atlas) +
                    " -e " + session +
                    " -s " + subject +
                    " -r \""+extension+"\" -o \"_tents\"")


