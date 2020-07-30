import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from typing import List
from classes import GLMs
from classes import Images
from abc import abstractmethod

#Last updated 02/27/20
# This class is a collection of GLM objects.
# The purpose of this class is to generalize as much as possible from all of the GLMs
# Then to place what cannot be generalized into the sub classes for each task

# When adding new GLMs they will probably be a type of event GLM
# you will want to create a new function in each the class you want to add a glm to,

# Start by adding an event_label to describe your event
# Then you'll want to create a new list of tuples named regressors models labels.
# regressors_models_labels = [(regressor1, model1, regressor_label1),(regressor2, model2, regressor_label2)]
# The regressors are the extension on the regressor files
# The model is the model that will be used on the regressor
# The label is what will be used to identify that particular regressor

# Then create another list of tuples that are contrasts and labels
# contrasts_labels = [(contrast1, contrast_label1), (contrast2, contrast_label2)]
# The contrasts will use the labels from regressor labels to do simple math between the different regressors
# The label will be the label of that contrast

# Next pass these two list of tuples as well as a description of the models into the generate_roistats_designs_postfixes function
# roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
#                                                                       contrasts_labels,
#                                                                       '_tents')
# This should automatically generate a list of tuples for each regressor and each contrast
# with the provided model description
# return should look something like this
# [(regressor_label1, '_tents'),(regressor_label2, '_tents'),(contrast_label1, '_tents'), (contrast_label1, '_tents')]
# Finally pass all the info into the build_glms function
# self.build_glms(glm_type=glm_type,
#                 glm_label=glm_label,
#                 regressors_models_labels=regressors_models_labels,
#                 contrasts_labels=contrasts_labels,
#                 roistats_designs_postfixes=roistats_designs_postfixes)
# This should return a tuple of three glms (Volume, Surface_L, Surface_R)
# make sure to add your new function to the create_events_glms function



image_list = List[Images.preprocessed_image]

#
class TaskGLMs(object):
    def __init__(self, working_dir, images: image_list):
        self.images = images
        self.subject = images[0].subject
        self.session = images[0].session
        self.task = images[0].task
        self.tr = images[0].tr
        self.TRpKnot = self.set_tr_per_knot()

        self.working_dir = working_dir
        self.buttonPress_model, self.button_idx = self.create_Tent_models(16.8)
        self.blockONandOFF_model, self.button_idx = self.create_Tent_models(16.8)
        self.block_model = "'dmBLOCK(1)'"
        self.hrf_model = "'BLOCK(2,1)'"
        self.hrf_idx = "0..0"
        self.ortvec = self.generate_ortvec()
        self.censor = self.generate_censor()

        return

    #Set The TR per knot for each of the TRs
    def set_tr_per_knot(self):
        if self.tr == 1.2:
            TRpKnot = 2
        elif self.tr == 0.8:
            TRpKnot = 3

        return TRpKnot

    # Every GLM that we are running is a censored glm all glms must have a censor file.
    def generate_censor(self, run_num=None):
        if not run_num:
            return os.path.join(self.working_dir, self.subject, 'INPUT_DATA', self.task, self.session,
                                'movregs_FD_mask.txt')
        else:
            return os.path.join(self.working_dir, self.subject, 'INPUT_DATA', self.task, self.session,
                                f'movregs_FD_mask_{run_num}.txt')

    # Every GLM that we are running must have an orthogan vector of the movement regressors.
    def generate_ortvec(self, run_num=None):
        if not run_num:
            return os.path.join(self.working_dir, self.subject, 'INPUT_DATA', self.task, self.session,
                                "motion_demean_" + self.session + ".1D")
        else:
            return os.path.join(self.working_dir, self.subject, 'INPUT_DATA', self.task, self.session,
                                f"motion_demean_{self.session}_{run_num}.1D")


    # builds the volumetric left and right hemisphere GLM given the glm type, label, regressor parameters and the contrast parameters
    # returns three glms in a tuple
    def build_glms(self, images=None, glm_type="", glm_label="", regressors_models_labels=[], contrasts_labels=[],
                   roistats_designs_postfixes=[], polort = 'A', generate_residuals=False):

        if images is None:
            images = self.images

        volume_glm = GLMs.VolumeGLM(images=images,
                                    working_dir=self.working_dir,
                                    glm_type=glm_type,
                                    glm_label=glm_label,
                                    censor=self.censor,
                                    polort=polort,
                                    generate_residuals=generate_residuals,
                                    regressors_models_labels=regressors_models_labels,
                                    contrasts_labels=contrasts_labels,
                                    ortvec=self.ortvec,
                                    roistats_designs_postfixes=roistats_designs_postfixes)

        surface_L_glm = GLMs.SurfaceGLM(images=images,
                                        working_dir=self.working_dir,
                                        glm_type=glm_type,
                                        glm_label=glm_label,
                                        force_tr=self.tr,
                                        censor=self.censor,
                                        polort=polort,
                                        generate_residuals=generate_residuals,
                                        regressors_models_labels=regressors_models_labels,
                                        contrasts_labels=contrasts_labels,
                                        hemisphere='L',
                                        ortvec=self.ortvec,
                                        roistats_designs_postfixes=roistats_designs_postfixes)

        surface_R_glm = GLMs.SurfaceGLM(images=images,
                                        working_dir=self.working_dir,
                                        glm_type=glm_type,
                                        glm_label=glm_label,
                                        force_tr=self.tr,
                                        censor=self.censor,
                                        polort=polort,
                                        generate_residuals=generate_residuals,
                                        regressors_models_labels=regressors_models_labels,
                                        contrasts_labels=contrasts_labels,
                                        hemisphere='R',
                                        ortvec=self.ortvec,
                                        roistats_designs_postfixes=roistats_designs_postfixes)

        return (volume_glm, surface_L_glm, surface_R_glm)

    # all the task use the on blocks glms with the same parameters in each one
    def create_on_blocks_glms(self):

        regressors_models_labels = [('block', self.block_model, 'ON_BLOCKS')]
        type = 'ON_BLOCKS'
        roistats_designs_postfixes = [('ON_BLOCKS', '_blocks')]

        return self.build_glms(glm_type=type,
                               regressors_models_labels=regressors_models_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    # all task have on mixed glms.
    # These glms have the same structure across tasks
    # but the event model changes across tasks
    def create_on_mixed_glms(self):
        type = 'ON_MIXED'
        regressors_models_labels = [("block", self.block_model, 'ON_BLOCKS'),
                                    ("blockONandOFF", self.blockONandOFF_model, "ON_blockONandOFF"),
                                    ("allTrials", self.event_model, "ON_TRIALS")]
        roistats_designs_postfixes = [('ON_BLOCKS', '_blocks'),
                                      ('ON_blockONandOFF', '_tents'),
                                      ('ON_TRIALS', '_tents')]

        return self.build_glms(glm_type=type,
                               regressors_models_labels=regressors_models_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    # Each taskGLMs collection will override this function to provide its own event GLMs
    # The event GLMs change the most across the subjects
    @abstractmethod
    def create_events_glms(self):
        '''To Override'''
        pass

    def create_Tent_models(self, duration):
        #is The duration evenly divisible by the TRpKnot * tr
        while not round(duration/self.tr, 2) % self.TRpKnot == 0:
            duration = duration + self.tr
        nonzero_knots = round(duration / (self.TRpKnot * float(self.tr)), 2)
        total_knots = nonzero_knots + 1
        model = f"'TENTzero(0,{round(duration, 2)},{int(total_knots)})'"
        final_index = total_knots - 3
        idx = f"0..{int(final_index)}"
        return model, idx

    # This will take a list of contrasts and regressors
    # and turn them into a list of tuples containing the model and the contrast or the single regressors
    def generate_roistats_designs_postfixes(self, contrasts, regressors, model):
        roistats_designs_postfixes = []
        for contrast in contrasts:
            roistats_designs_postfixes.append((contrast[-1], model))
        for regressor in regressors:
            roistats_designs_postfixes.append((regressor[-1], model))

        return roistats_designs_postfixes

#TODO Tent models will need to be changed based on MB Think about tr value, duration, mb8, and TR per knot

class AxcptGLMs(TaskGLMs):
    def __init__(self, working_dir, images: image_list):
        TaskGLMs.__init__(self, working_dir, images)
        self.tent_duration = 21.6
        self.event_model, self.idx = self.create_Tent_models(duration=self.tent_duration)
        self.glms = []
        self.glms.append(self.create_on_blocks_glms())
        self.glms.append(self.create_on_mixed_glms())
        self.glms.extend(self.create_events_glms())

        return

    def create_cues_events_glm(self, glm_type):
        # This is for the the traditional glms

        generate_residuals = False
        glm_label = f"Cues"
        regressors_models_labels = [(f"block", self.block_model, f"block"),
                                    (f"blockONandOFF", self.blockONandOFF_model, f"blockONandOFF"),
                                    (f"AX", self.event_model, f"AX"),
                                    (f"AY", self.event_model, f"AY"),
                                    (f"Ang", self.event_model, f"Ang"),
                                    (f"BX", self.event_model, f"BX"),
                                    (f"BY", self.event_model, f"BY"),
                                    (f"Bng", self.event_model, f"Bng")]

        contrasts_labels = [(
            f"+0.5*AX[[{self.idx}]] +0.5*AY[[{self.idx}]] -0.5*BX[[{self.idx}]] -0.5*BY[[{self.idx}]]",
            "Acue_Bcue"),
            (
                f"+0.5*AY[[{self.idx}]] +0.5*BX[[{self.idx}]] -0.5*AX[[{self.idx}]] -0.5*BY[[{self.idx}]]",
                "HI_LO_conf"),
            (
                f"+0.5*Ang[[{self.idx}]] +0.5*Bng[[{self.idx}]] -0.25*AX[[{self.idx}]] -0.25*AY[[{self.idx}]] -0.25*BX[[{self.idx}]] -0.25*BY[[{self.idx}]]",
                "Nogo_Go")
        ]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=generate_residuals)


    def create_cues_events_glm_single_run(self, glm_type, image=None):

        evt_appendix=f"_{image.run_num}"
        generate_residuals = True
        glm_label = f"Cues{evt_appendix}"

        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, f"block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, f"blockONandOFF"),
                                    (f"AX{evt_appendix}", self.event_model, f"AX"),
                                    (f"AY{evt_appendix}", self.event_model, f"AY"),
                                    (f"Ang{evt_appendix}", self.event_model, f"Ang"),
                                    (f"BX{evt_appendix}", self.event_model, f"BX"),
                                    (f"BY{evt_appendix}", self.event_model, f"BY"),
                                    (f"Bng{evt_appendix}", self.event_model, f"Bng"),
                                    (f"error{evt_appendix}", self.event_model, f"error")]

        contrasts_labels = [(
            f"+0.5*AX[[{self.idx}]] +0.5*AY[[{self.idx}]] -0.5*BX[[{self.idx}]] -0.5*BY[[{self.idx}]]",
            "Acue_Bcue"),
            (
                f"+0.5*AY[[{self.idx}]] +0.5*BX[[{self.idx}]] -0.5*AX[[{self.idx}]] -0.5*BY[[{self.idx}]]",
                "HI_LO_conf"),
            (
                f"+0.5*Ang[[{self.idx}]] +0.5*Bng[[{self.idx}]] -0.25*AX[[{self.idx}]] -0.25*AY[[{self.idx}]] -0.25*BX[[{self.idx}]] -0.25*BY[[{self.idx}]]",
                "Nogo_Go"),
            (
                f"+error[[{self.idx}]] -0.25*AX[[{self.idx}]] -0.25*AY[[{self.idx}]] -0.25*BX[[{self.idx}]] -0.25*BY[[{self.idx}]]",
                "error_correct")
        ]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(images=[image],
                               glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=generate_residuals)

    def create_buttons_events_glm(self, glm_type):
        generate_residuals = False

        glm_label = f"Buttons"
        regressors_models_labels = [(f"block", self.block_model, "block"),
                                    (f"blockONandOFF", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"button1", self.buttonPress_model, "button1"),
                                    (f"button2", self.buttonPress_model, "button2")]

        contrasts_labels = [("+button1[[" + self.button_idx + "]] -button2[[" + self.button_idx + "]]", "B1_B2")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    def create_buttons_events_glm_single_run(self, glm_type, image=None):

        evt_appendix=f"_{image.run_num}"
        glm_label = f"Buttons{evt_appendix}"


        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, "block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"button1{evt_appendix}", self.buttonPress_model, "button1"),
                                    (f"button2{evt_appendix}", self.buttonPress_model, "button2"),
                                    (f"error{evt_appendix}", self.event_model, f"error")]

        contrasts_labels = [(f"+button1[[{self.button_idx}]] -button2[[{self.button_idx}]]", "B1_B2"),
                            (f"+error[[{self.idx}]] -0.5*button1[[{self.idx}]] -0.5*button2[[{self.idx}]]", "error_correct")
                            ]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(images=[image],
                               glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=True)

    # This will create the event glms and return a list of tuples
    # so glms may look like this
    # event_glms=[(volume_event_glm1,surface_L_event_glm1,surface_R_event_glm1),
    #             (volume_event_glm2,surface_L_event_glm2,surface_R_event_glm2)]
    def create_events_glms(self):
        event_glms = []
        glm_type = "EVENTS"
        event_glms.append(self.create_buttons_events_glm(glm_type))
        event_glms.append(self.create_cues_events_glm(glm_type))
        for image in self.images:
            self.ortvec = self.generate_ortvec(run_num=image.run_num)
            self.censor = self.generate_censor(run_num=image.run_num)
            event_glms.append(self.create_cues_events_glm_single_run(glm_type, image))
            event_glms.append(self.create_buttons_events_glm_single_run(glm_type, image))
        return event_glms


class CuedtsGLMs(TaskGLMs):
    def __init__(self, working_dir, images: image_list):
        TaskGLMs.__init__(self, working_dir, images)
        self.tent_duration = 24
        self.event_model, self.idx = self.create_Tent_models(duration=self.tent_duration)
        self.glms = []
        self.glms.append(self.create_on_blocks_glms())
        self.glms.append(self.create_on_mixed_glms())
        self.glms.extend(self.create_events_glms())

        return

    def create_incentive_event_glm(self, type):
        glm_label = "Incentive"
        regressors_models_labels = [("block", self.block_model, "block"),
                                    ("blockONandOFF", self.blockONandOFF_model, "blockONandOFF"),
                                    ("Inc", self.event_model, "Inc"),
                                    ("NoInc", self.event_model, "NoInc")]

        contrasts_labels = [("+Inc[[" + self.idx + "]] -NoInc[[" + self.idx + "]]", "Inc_NoInc")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(glm_type=type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    def create_congruency_incentive_event_glm(self, type):
        glm_label = "CongruencyIncentive"

        regressors_models_labels = [("block", self.block_model, "block"),
                                    ("blockONandOFF", self.blockONandOFF_model, "blockONandOFF"),
                                    ("ConInc", self.event_model, "ConInc"),
                                    ("ConNoInc", self.event_model, "ConNoInc"),
                                    ("InConInc", self.event_model, "InConInc"),
                                    ("InConNoInc", self.event_model, "InConNoInc")]
        contrasts_labels = [(
            "+0.5*ConInc[[" + self.idx + "]] +0.5*InConInc[[" + self.idx + "]] -0.5*ConNoInc[[" + self.idx + "]] -0.5*InConNoInc[[" + self.idx + "]]",
            "Inc_NoInc"),
            (
                "+0.5*InConInc[[" + self.idx + "]] +0.5*InConNoInc[[" + self.idx + "]] -0.5*ConInc[[" + self.idx + "]] -0.5*ConNoInc[[" + self.idx + "]]",
                "InCon_Con")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(glm_type=type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    def create_letter_number_event_glm(self, glm_type):
        glm_label = "LetterNumber"
        regressors_models_labels = [("block", self.block_model, "block"),
                                    ("blockONandOFF", self.blockONandOFF_model, "blockONandOFF"),
                                    ("letter", self.event_model, "letter"),
                                    ("number", self.event_model, "number")]
        contrasts_labels = [("+letter[[" + self.idx + "]] -number[[" + self.idx + "]]", "Let_Num")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    def create_buttons_event_glm(self, glm_type):
        glm_label = "Buttons"
        regressors_models_labels = [("block", self.block_model, "block"),
                                    ("blockONandOFF", self.blockONandOFF_model, "blockONandOFF"),
                                    ("button1", self.buttonPress_model, "button1"),
                                    ("button2", self.buttonPress_model, "button2")]
        contrasts_labels = [("+button1[[" + self.button_idx + "]] -button2[[" + self.button_idx + "]]", "B1_B2")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    def create_incentive_event_glm_single_run(self, glm_type, image=None):
        evt_appendix = f"_{image.run_num}"
        glm_label = f"Incentive{evt_appendix}"

        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, "block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"Inc{evt_appendix}", self.event_model, "Inc"),
                                    (f"NoInc{evt_appendix}", self.event_model, "NoInc"),
                                    (f"error{evt_appendix}", self.event_model, f"error")]

        contrasts_labels = [(f"+Inc[[{self.idx}]] -NoInc[[{self.idx}]]", "Inc_NoInc"),
                            (f"+error[[{self.idx}]] -0.5*Inc[[{self.idx}]] -0.5*NoInc[[{self.idx}]]", "error_correct")
                            ]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(images=[image],
                               glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=True)

    def create_congruency_incentive_event_glm_single_run(self, glm_type, image=None):
        evt_appendix = f"_{image.run_num}"
        glm_label = f"CongruencyIncentive{evt_appendix}"

        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, "block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"ConInc{evt_appendix}", self.event_model, "ConInc"),
                                    (f"ConNoInc{evt_appendix}", self.event_model, "ConNoInc"),
                                    (f"InConInc{evt_appendix}", self.event_model, "InConInc"),
                                    (f"InConNoInc{evt_appendix}", self.event_model, "InConNoInc"),
                                    (f"error{evt_appendix}", self.event_model, f"error")]
        contrasts_labels = [(
            f"+0.5*ConInc[[{self.idx}]] +0.5*InConInc[[{self.idx}]] -0.5*ConNoInc[[{self.idx}]] -0.5*InConNoInc[[{self.idx}]]",
            "Inc_NoInc"),
            (
                f"+0.5*InConInc[[{self.idx}]] +0.5*InConNoInc[[{self.idx}]] -0.5*ConInc[[{self.idx}]] -0.5*ConNoInc[[{self.idx}]]",
                "InCon_Con"),
            (
                f"+error[[{self.idx}]] -0.25*ConInc[[{self.idx}]] -0.25*ConNoInc[[{self.idx}]] -0.25*InConInc[[{self.idx}]] -0.25*InConNoInc[[{self.idx}]]",
                "error_correct")
        ]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(images=[image],
                               glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=True)

    def create_letter_number_event_glm_single_run(self, glm_type, image=None):
        evt_appendix = f"_{image.run_num}"
        glm_label = f"LetterNumber{evt_appendix}"

        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, "block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"letter{evt_appendix}", self.event_model, "letter"),
                                    (f"number{evt_appendix}", self.event_model, "number"),
                                    (f"error{evt_appendix}", self.event_model, f"error")
                                    ]
        contrasts_labels = [(f"+letter[[{self.idx}]] -number[[{self.idx}]]", "Let_Num"),
                            (f"+error[[{self.idx}]] -0.5*letter[[{self.idx}]] -0.5*number[[{self.idx}]]", "error_correct")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(images=[image],
                               glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=True)

    def create_buttons_event_glm_single_run(self, glm_type, image):

        evt_appendix=f"_{image.run_num}"
        glm_label = f"Buttons{evt_appendix}"

        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, "block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"button1{evt_appendix}", self.buttonPress_model, "button1"),
                                    (f"button2{evt_appendix}", self.buttonPress_model, "button2"),
                                    (f"error{evt_appendix}", self.event_model, f"error")
                                    ]
        contrasts_labels = [("+button1[[" + self.button_idx + "]] -button2[[" + self.button_idx + "]]", "B1_B2"),
                            (f"+error[[{self.idx}]] -0.5*button1[[{self.idx}]] -0.5*button2[[{self.idx}]]", "error_correct")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(images=[image],
                               glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=True)


    def create_events_glms(self):
        event_glms = []

        glm_type = "EVENTS"

        event_glms.append(self.create_letter_number_event_glm(glm_type))
        event_glms.append(self.create_buttons_event_glm(glm_type))
        event_glms.append(self.create_incentive_event_glm(glm_type))
        event_glms.append(self.create_congruency_incentive_event_glm(glm_type))
        for image in self.images:
            self.generate_ortvec(run_num=image.run_num)
            self.generate_censor(run_num=image.run_num)
            event_glms.append(self.create_letter_number_event_glm_single_run(glm_type, image))
            event_glms.append(self.create_buttons_events_glm_single_run(glm_type, image))
            event_glms.append(self.create_incentive_event_glm_single_run(glm_type, image))
            event_glms.append(self.create_congruency_incentive_event_glm_single_run(glm_type, image))

        return event_glms


class SternGLMs(TaskGLMs):
    def __init__(self, working_dir, images: image_list):
        TaskGLMs.__init__(self, working_dir, images)
        self.tent_duration = 26.4
        self.event_model, self.idx = self.create_Tent_models(duration=self.tent_duration)
        self.glms = []
        self.glms.append(self.create_on_blocks_glms())
        self.glms.append(self.create_on_mixed_glms())
        self.glms.extend(self.create_events_glms())

    def create_list_length_events_glms(self, glm_type):
        glm_label = "ListLength"
        regressors_models_labels = [("block", self.block_model, "block"),
                                    ("blockONandOFF", self.blockONandOFF_model, "blockONandOFF"),
                                    ("LL5NP", self.event_model, "LL5NP"),
                                    ("LL5NN", self.event_model, "LL5NN"),
                                    ("LL5RN", self.event_model, "LL5RN"),
                                    ("not5NP", self.event_model, "not5NP"),
                                    ("not5NN", self.event_model, "not5NN"),
                                    ("not5RN", self.event_model, "not5RN")]

        contrasts_labels = [(
            f"+0.5*LL5RN[[{self.idx}]] +0.5*not5RN[[{self.idx}]] -0.5*LL5NN[[{self.idx}]] -0.5*not5NN[[{self.idx}]]",
            "RN_NN_all"),
            (f"+LL5RN[[{self.idx}]] -LL5NN[[{self.idx}]]", "RN_NN_LL5"),
            (f"+not5RN[[{self.idx}]] -not5NN[[{self.idx}]]", "RN_NN_not5"),
            (
            f"+0.33*not5NP[[{self.idx}]] +0.33*not5NN[[{self.idx}]] +0.33*not5RN[[{self.idx}]] -0.33*LL5NP[[{self.idx}]] -0.33*LL5NN[[{self.idx}]] -0.33*LL5RN[[{self.idx}]]",
            "not5_LL5")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    # subtype of Event_GLMs that need to be created
    def create_buttons_events_glms(self, glm_type):
        glm_label = "Buttons"
        regressors_models_labels = [("block", self.block_model, "block"),
                                    ("blockONandOFF", self.blockONandOFF_model, "blockONandOFF"),
                                    ("button1", self.buttonPress_model, "button1"),
                                    ("button2", self.buttonPress_model, "button2")]

        contrasts_labels = [
            (f"+button1[[{self.button_idx}]] -button2[[{self.button_idx}]]", "B1_B2")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)


    def create_list_length_events_glms_single_run(self, glm_type, image):
        evt_appendix=f"_{image.run_num}"
        glm_label = f"ListLength{evt_appendix}"

        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, "block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"LL5NP{evt_appendix}", self.event_model, "LL5NP"),
                                    (f"LL5NN{evt_appendix}", self.event_model, "LL5NN"),
                                    (f"LL5RN{evt_appendix}", self.event_model, "LL5RN"),
                                    (f"not5NP{evt_appendix}", self.event_model, "not5NP"),
                                    (f"not5NN{evt_appendix}", self.event_model, "not5NN"),
                                    (f"not5RN{evt_appendix}", self.event_model, "not5RN"),
                                    (f"error{evt_appendix}", self.event_model, "error")]
        contrasts_labels = [(
            f"+0.5*LL5RN[[{self.idx}]] +0.5*not5RN[[{self.idx}]] -0.5*LL5NN[[{self.idx}]] -0.5*not5NN[[{self.idx}]]",
            "RN_NN_all"),
            (f"+LL5RN[[{self.idx}]] -LL5NN[[{self.idx}]]", "RN_NN_LL5"),
            (f"+not5RN[[{self.idx}]] -not5NN[[{self.idx}]]", "RN_NN_not5"),
            (
            f"+0.33*not5NP[[{self.idx}]] +0.33*not5NN[[{self.idx}]] +0.33*not5RN[[{self.idx}]] -0.33*LL5NP[[{self.idx}]] -0.33*LL5NN[[{self.idx}]] -0.33*LL5RN[[{self.idx}]]",
            "not5_LL5"),
            (f"+error[[{self.idx}]] -0.167*LL5NP[[{self.idx}]] -0.167*LL5NN[[{self.idx}]] -0.167*LL5RN[[{self.idx}]] -0.167*not5NP[[{self.idx}]] -0.167*not5NN[[{self.idx}]] -0.167*not5RN[[{self.idx}]]", "error_correct")
        ]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(images=[image],
                               glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=True)

    # subtype of Event_GLMs that need to be created
    def create_buttons_events_glms_single_run_glm(self, glm_type, image):
        evt_appendix = f"_{image.run_num}"
        glm_label = f"Buttons{evt_appendix}"
        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, "block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"button1{evt_appendix}", self.buttonPress_model, "button1"),
                                    (f"button2{evt_appendix}", self.buttonPress_model, "button2")]

        contrasts_labels = [
            (f"+button1[[{self.button_idx}]] -button2[[{self.button_idx}]]", "B1_B2"),
            (f"+error[[{self.idx}]] -0.5*button1[[{self.idx}]] -0.5*button2[[{self.idx}]]", "error_correct")]

        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              '_tents')

        return self.build_glms(images=[image],
                               glm_type=glm_type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=True)


    def create_events_glms(self):
        glm_type = "EVENTS"
        event_glms = []
        event_glms.append(self.create_buttons_events_glms(glm_type))
        event_glms.append(self.create_list_length_events_glms(glm_type))
        for image in self.images:
            self.ortvec = self.generate_ortvec(run_num=image.run_num)
            self.censor = self.generate_censor(run_num=image.run_num)
            event_glms.append(self.create_buttons_events_glms_single_run_glm(glm_type, image))
            event_glms.append(self.create_list_length_events_glms_single_run(glm_type, image))
        return event_glms


class StroopGLMs(TaskGLMs):
    def __init__(self, working_dir, images: image_list):
        TaskGLMs.__init__(self, working_dir, images)
        self.tent_duration = 16.8
        self.event_model, self.idx = self.create_Tent_models(duration=self.tent_duration)
        self.glms = []
        self.glms.append(self.create_on_blocks_glms())
        self.glms.append(self.create_on_mixed_glms())
        self.glms.extend(self.create_events_glms())
        self.glms.extend(self.create_events_glms(HRF_EVENTS=True))

        return

    def create_congruency_events_glms(self, type, idx, model):
        glm_label = "Congruency"

        regressors_models_labels = [("block", self.block_model, "block"),
                                    ("blockONandOFF", self.blockONandOFF_model, "blockONandOFF"),
                                    ("PC50Con", model, "PC50Con"),
                                    ("PC50InCon", model, "PC50InCon"),
                                    ("biasCon", model, "biasCon"),
                                    ("biasInCon", model, "biasInCon")]

        if self.images[0].session == 'reactive':
            regressors_models_labels.append(("buffCon", model, "buffCon"))

        contrasts_labels = [(f"+biasInCon[[{idx}]] -biasCon[[{idx}]]", "InCon_Con_bias"),
                            (f"+PC50InCon[[{idx}]] -PC50Con[[{idx}]]", "InCon_Con_PC50"),
                            (f"+0.5*biasInCon[[{idx}]] +0.5*PC50InCon[[{idx}]] -0.5*biasCon[[{idx}]] -0.5*PC50Con[[{idx}]]",
                             "InCon_Con_PC50bias")]

        if type == "HRF_EVENTS":
            model = '_HRF'
        else:
            model = '_tents'
        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              model)

        return self.build_glms(glm_type=type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes)

    def create_congruency_events_glms_single_run(self, type, idx, model, image):
        evt_appendix=f"_{image.run_num}"
        glm_label = f"Congruency{evt_appendix}"

        regressors_models_labels = [(f"block{evt_appendix}", self.block_model, "block"),
                                    (f"blockONandOFF{evt_appendix}", self.blockONandOFF_model, "blockONandOFF"),
                                    (f"PC50Con{evt_appendix}", model, "PC50Con"),
                                    (f"PC50InCon{evt_appendix}", model, "PC50InCon"),
                                    (f"biasCon{evt_appendix}", model, "biasCon"),
                                    (f"biasInCon{evt_appendix}", model, "biasInCon")]


        contrasts_labels = [(f"+biasInCon[[{idx}]] -biasCon[[{idx}]]", "InCon_Con_bias"),
                            (f"+PC50InCon[[{idx}]] -PC50Con[[{idx}]]", "InCon_Con_PC50"),
                            (f"+0.5*biasInCon[[{idx}]] +0.5*PC50InCon[[{idx}]] -0.5*biasCon[[{idx}]] -0.5*PC50Con[[{idx}]]",
                             "InCon_Con_PC50bias")]

        if self.images[0].session == 'reactive':
            regressors_models_labels.append((f"buffCon{evt_appendix}", model, "buffCon"))
            contrasts_labels.append((f"+error[[{self.idx}]] -0.2*PC50Con[[{self.idx}]] -0.2*PC50InCon[[{self.idx}]] -0.2*biasCon[[{self.idx}]] -0.2*biasInCon[[{self.idx}]] -0.2*buffCon[[{self.idx}]]", "error_correct"))
        else:
            contrasts_labels.append((
                                    f"+error[[{self.idx}]] -0.25*PC50Con[[{self.idx}]] -0.25*PC50InCon[[{self.idx}]] -0.25*biasCon[[{self.idx}]] -0.25*biasInCon[[{self.idx}]]",
                                    "error_correct"))
        if type == "HRF_EVENTS":
            model = '_HRF'
        else:
            model = '_tents'
        roistats_designs_postfixes = self.generate_roistats_designs_postfixes(regressors_models_labels,
                                                                              contrasts_labels,
                                                                              model)

        return self.build_glms(images=[image],
                               glm_type=type,
                               glm_label=glm_label,
                               regressors_models_labels=regressors_models_labels,
                               contrasts_labels=contrasts_labels,
                               roistats_designs_postfixes=roistats_designs_postfixes,
                               generate_residuals=True)

    def create_events_glms(self, HRF_EVENTS=False):

        if HRF_EVENTS:

            type = "HRF_EVENTS"
            idx = self.hrf_idx
            model = self.hrf_model

        else:

            type = "EVENTS"
            idx = self.idx
            model = self.event_model

        event_glms = []

        event_glms.append(self.create_congruency_events_glms(type, idx, model))
        for image in self.images:
            self.ortvec = self.generate_ortvec(run_num=image.run_num)
            self.censor = self.generate_censor(run_num=image.run_num)
            event_glms.append(self.create_congruency_events_glms_single_run(type, idx, model, image))
            self.ortvec = self.generate_ortvec()
            self.censor = self.generate_censor()
        return event_glms
