import os
import RunShellFunc as rs
import ConfigGLMs


def block_glms(working_dir, subject, task, session):
    print("Running Volume Block GLMs: " + subject + " " + session + " " + task)
    model =[ConfigGLMs.Block]
    regressor = ['block']
    label = ['ON_BLOCKS']
    glmMaker(working_dir=working_dir, subject=subject, task=task, session=session,
            regressor=regressor, regressor_label=label,  regressor_model=model,
            type='ON_BLOCKS')


def mixed_glms(working_dir, subject, task, session):

    print("Running Volume Mixed GLMs: " + subject + " " + session + " " + task)

    label_blocks = "ON_BLOCKS"
    label_on_off = "ON_blockONandOFF"
    label_events = "ON_TRIALS"
    model_block = ConfigGLMs.Block
    model_on_off = ConfigGLMs.blockONandOFF
    regressor_blocks = "block"
    regressor_on_off = "blockONandOFF"
    regressor_events = "allTrials"

    if task == 'Axcpt':
        model_event=ConfigGLMs.AxcptEventTent
        index = ConfigGLMs.AxcptEventTent

    if task == 'Cuedts':
        model_event = ConfigGLMs.CuedtsEventTent
        index = ConfigGLMs.CuedtsEventTent

    if task == 'Stern':
        model_event = ConfigGLMs.SternEventTent
        index = ConfigGLMs.SternEventTent

    if task == 'Stroop':
        model_event = ConfigGLMs.StroopEventTent
        index = ConfigGLMs.StroopEventTent

    labels = [label_blocks, label_on_off, label_events]
    models = [model_block, model_on_off, model_event]
    regressors = [regressor_blocks, regressor_on_off, regressor_events]

    glmMaker(working_dir=working_dir, subject=subject, task=task, session=session,
            regressor=regressors, regressor_label=labels,  regressor_model=models,
            type='ON_MIXED')


def event_glms(working_dir, subject, task, session):
    print("Running Volume Event GLMs: " + subject + " " + session + " " + task)

    if task == 'Axcpt':
        event_regressors = ConfigGLMs.AxcptEventRegressors
        glm_labels = ConfigGLMs.AxcptEventGLMLabels
        event_contrasts = ConfigGLMs.AxcptEventContrasts
        event_contrast_glm_ids = ConfigGLMs.AxcptEventContrastsGLMids
        event_contrast_labels = ConfigGLMs.AxcptEventContrastLabels
        models = ConfigGLMs.AxcptEventModels
        index = ConfigGLMs.AxcptEventIDX

    if task == 'Cuedts':
        event_regressors = ConfigGLMs.CuedtsEventRegressors
        glm_labels = ConfigGLMs.CuedtsEventGLMLabels
        event_contrasts = ConfigGLMs.CuedtsEventContrasts
        event_contrast_glm_ids = ConfigGLMs.CuedtsEventContrastsGLMids
        event_contrast_labels = ConfigGLMs.CuedtsEventContrastLabels
        models = ConfigGLMs.CuedtsEventModels
        index = ConfigGLMs.CuedtsEventIDX

    if task == 'Stern':
        event_regressors = ConfigGLMs.SternEventRegressors
        glm_labels = ConfigGLMs.SternEventGLMLabels
        event_contrasts = ConfigGLMs.SternEventContrasts
        event_contrast_glm_ids = ConfigGLMs.SternEventContrastsGLMids
        event_contrast_labels = ConfigGLMs.SternEventContrastLabels
        models = ConfigGLMs.SternEventModels
        index = ConfigGLMs.SternEventIDX

    if task == 'Stroop':
        event_regressors = ConfigGLMs.StroopEventRegressors
        glm_labels = ConfigGLMs.StroopEventGLMLabels
        event_contrasts = ConfigGLMs.StroopEventContrasts
        event_contrast_glm_ids = ConfigGLMs.StroopEventContrastsGLMids
        event_contrast_labels = ConfigGLMs.StroopEventContrastLabels
        models = ConfigGLMs.StroopEventModels
        index = ConfigGLMs.StroopEventIDX

        if session == 'reactive':
            event_regressors = ConfigGLMs.StroopReaEventRegressors
            models = ConfigGLMs.StroopReaEventModels

    event_contrasts = [c.replace("idx_buttons", ConfigGLMs.buttonIDX) for c in event_contrasts]
    event_contrasts = [c.replace("idx", index) for c in event_contrasts]

    for i in range(len(glm_labels)):
        contrast_labels = []
        contrasts = []
        for j in range(len(event_contrast_glm_ids)):
            if event_contrast_glm_ids[j] == glm_labels[i]:
                contrast_labels.append(event_contrast_labels[j])
                contrasts.append(event_contrasts[j])
        glmMaker(working_dir=working_dir, subject=subject, task=task, session=session,
                 regressor=event_regressors[i].split(), regressor_label=event_regressors[i].split(), regressor_model=models[i].split(),
                 contrast=contrasts, contrast_label=contrast_labels,
                 type='EVENTS', glm_label=glm_labels[i])


def single_regressor_glm(working_dir, subject, task, session):
    print("Running Volume Single Regressor GLMs: " + subject + " " + session + " " + task)

    if task == 'Stroop':
        event_regressors = ConfigGLMs.StroopEventRegressors
        glm_labels = ConfigGLMs.StroopEventGLMLabels
        event_contrasts = ConfigGLMs.StroopEventContrasts
        event_contrast_glm_ids = ConfigGLMs.StroopSingleRegressorGLMids
        event_contrast_labels = ConfigGLMs.StroopEventContrastLabels
        models = ConfigGLMs.StroopSingleRegressorModels
        index = ConfigGLMs.HRFIDX

        if session == 'reactive':
            event_regressors = ConfigGLMs.StroopReaEventRegressors
            models = ConfigGLMs.StroopReaSingleRegressorModels


        event_contrasts = [c.replace("idx_buttons", ConfigGLMs.buttonIDX) for c in event_contrasts]
        event_contrasts = [c.replace("idx", index) for c in event_contrasts]

        for i in range(len(glm_labels)):
            contrast_labels = []
            contrasts = []
            for j in range(len(event_contrast_glm_ids)):
                if event_contrast_glm_ids[j] == glm_labels[i]:
                    contrast_labels.append(event_contrast_labels[j])
                    contrasts.append(event_contrasts[j])

            glmMaker(working_dir=working_dir, subject=subject, task=task, session=session,
                     regressor=event_regressors[i].split(), regressor_label=event_regressors[i].split(), regressor_model=models[i].split(),
                     contrast=contrasts, contrast_label=contrast_labels,
                     type='HRF_EVENTS', glm_label=glm_labels[i])


def glmMaker(working_dir, subject, task, session, regressor, regressor_label, regressor_model, type, glm_label="", contrast=[], contrast_label=[]):
    #Inputs for the glmMaker
    #working dir --the top level directory where all the work will be done. This would be analogous to /scratch1/${USERNAME}/DMCCPILOT/AFNI_ANALYSIS
    #subject -- the subject number in string format
    #task -- The task name
    #session -- the session name
    #regressor -- the list of regresors that will be put into this glm
    #regressor label -- the list of labels that correspond to the regressors
    #regressor model -- the list of models to be used for each regressor
    #type -- the tag that will describe the type of glm that is being ran eg: EVENTS, ON_MIXED, HRF_EVENTS, ON_BLOCKS
    #glm_label -- describes the more specific type of glm that is being ran. each task will have is own set of glm labels
    #contrast -- the list of contrasts that will be used in the 3dremlfit
    #contrast_label -- the list of labels corresponding to the contrasts



    #Get the Inputs for the GLMs they should be AP and PA matched
    #TODO Check for correct run Number
    File1 = os.path.join(working_dir, subject, 'INPUT_DATA', task, session,
                         'lpi_scale_blur4_tfMRI_' + task + session[0:3].title() + '1_AP.nii.gz')
    File2 = os.path.join(working_dir, subject, 'INPUT_DATA', task, session,
                         'lpi_scale_blur4_tfMRI_' + task + session[0:3].title() + '2_PA.nii.gz')
    #combine them together in a single string for running the glm
    INPUT = File1 + ' ' + File2

    #alter the glm name so that we can mae a directory with the correct '_'
    if not glm_label == "":
        glm_label = "_"+glm_label

    #If the Directory Doesnt exist make it
    if not os.path.exists(os.path.join(working_dir, subject, 'RESULTS', task, session + glm_label + '_' + type + '_censored')):
        os.makedirs(os.path.join(working_dir, subject, 'RESULTS', task, session + glm_label + '_' + type + '_censored'))

    #move into that directory
    os.chdir(os.path.join(working_dir, subject, 'RESULTS', task, session + glm_label + '_' + type + '_censored'))

    #Build the beginning of the command
    command = "3dDeconvolve -local_times -x1D_stop \
    -GOFORIT 5 \
    -input " + INPUT + " \
    -polort A -float \
    -censor " + os.path.join(working_dir, subject, 'INPUT_DATA', task, session, 'movregs_FD_mask.txt') + " \
    -num_stimts " + str(len(regressor)) + " \
    -stim_times_AM1 1 " + os.path.join(working_dir, subject, 'INPUT_DATA', task, session,
                                           subject + '_' + task + '_' + session + '_'+regressor[0]+'.txt') + " " + regressor_model[0] + " -stim_label 1 " + regressor_label[0] + " \\"

#Add in the variable amount of stim times with their labels models and file names
    for i in range(len(regressor)-1):
        command = command + "-stim_times " + str(i+2) + " " + \
            os.path.join(working_dir, subject, 'INPUT_DATA', task, session, subject + '_' + task + '_' + session +
                                   '_' + regressor[i+1] + '.txt') + " "+regressor_model[i+1]+" -stim_label " + str(i+2) + " " + regressor_label[i+1] +" \\"

    command = command + "-ortvec " + os.path.join(working_dir, subject, 'INPUT_DATA', task, session, "motion_demean_"+session+".1D") + " movregs \
    -x1D X.xmat.1D -xjpeg X.jpg \
    -nobucket"

    rs.run_shell_command(command)

    command = "3dREMLfit -matrix X.xmat.1D \
    -GOFORIT 5 \
    -input '" + INPUT + "' \\"

    for i in range(len(contrast_label)):
        command = command + "-gltsym 'SYM: " + contrast[i] + "' " + contrast_label[i] +" \\"

    command = command + "-Rvar stats_var_"+subject+"_REML.nii.gz \
    -Rbuck STATS_"+subject+"_REML.nii.gz \
    -fout \
    -tout \
    -nobout \
    -verb"
    rs.run_shell_command(command)

