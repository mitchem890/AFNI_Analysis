import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from abc import ABCMeta, abstractmethod
from classes import Roistats, BashCommand


# This is the generalized GLM class
# Each GLM contains multiple roistats
# running the glm command through print will print info about that glm
# If you want to add glms I would not add them here.
# I would add them at the taskGLMs section for each task instead
class GLM(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):

        prop_defaults = {
            "images": None,
            "glm_type": "",
            "glm_label": "",
            "input": "path/to/scan1 /path/to/scan2",
            "force_tr": None,
            "hemisphere": None,
            "polort": 'A',
            "censor": "/path/to/censorFile",
            "regressors_models_labels": [],
            "ortvec": "/path/to/MovementFile",
            "contrasts_labels": [],
            "extension": ".nii.gz",
            "roistats_designs_postfixes": []
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.subject = self.images[0].subject
        self.session = self.images[0].session
        self.task = self.images[0].task
        self.image_dim = self.images[0].image_dim
        self.fsaverage = self.images[0].fsaverage
        self.input = self.generate_input()
        self.output_dir = self.generate_output_dir()
        self.regressors_models_labels = self.add_path_regressors_models_labels()
        self.roistats = self.generate_roistats()

        return

    # This will build a list of tuples of equal size
    # adding a path to each of the regressors along the way
    # This Will return a list of tuples of stings
    def add_path_regressors_models_labels(self):
        full_path_regressors_models_labels = []
        for item in self.regressors_models_labels or []:
            full_path_regressors_models_labels.append((self.generate_regressor_file_name(item[0]), item[1], item[2]))
        return full_path_regressors_models_labels

    # This will build the standard path way to the regressor filenames
    # returns string
    def generate_regressor_file_name(self, regressor):
        return os.path.join(self.working_dir, self.subject, 'INPUT_DATA', self.task, self.session,
                            f"{self.subject}_{self.task}_{self.session}_{regressor}.txt")

    # This will generate the output dir for the GLM
    def generate_output_dir(self):
        temp_glm_label = self.glm_label
        if not self.glm_label == "":
            temp_glm_label = f"_{self.glm_label}"
        return os.path.join(self.working_dir, self.subject, self.results_dir, self.task,
                            f'{self.session}{temp_glm_label}_{self.glm_type}_censored')

    # This will return a list of all the roistats for this glm
    def generate_roistats(self):
        roistats = []
        for item in self.roistats_designs_postfixes:
            roistats.extend(Roistats.build_roistats(input_file=os.path.join(self.output_dir, self.Rbuck),
                                                    design=item[0],
                                                    working_dir=self.output_dir,
                                                    session=self.session,
                                                    subject=self.subject,
                                                    image_dim=self.image_dim,
                                                    hemisphere=self.hemisphere,
                                                    postfix=item[1],
                                                    fsaverage=self.fsaverage))
        return roistats

    def __str__(self):
        return f"""{self.subject} {self.session} {self.task} {self.style} GLM: {self.glm_label}_{self.glm_type}"""

    @abstractmethod
    def generate_input(self):
        '''To Override'''
        pass


class VolumeGLM(GLM):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        prop_defaults = {
            "images": None,
            "working_dir": None,
            "glm_type": "",
            "glm_label": "",
            "force_tr": None,
            "hemisphere": None,
            "generate_residuals": False,
            "polort": 'A',
            "censor": "/path/to/censorFile",
            "regressors_models_labels": [],
            "ortvec": "/path/to/MovementFile",
            "contrasts_labels": [],
            "roistats_designs_postfixes": [],
            "extension": ".nii.gz"
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))



        self.style = "Volume"
        self.results_dir = "1TRpK_RESULTS"


        self.input = self.generate_input()
        self.Rvar = f"stats_var_{self.images[0].subject}_REML.nii.gz"
        self.Rbuck = f"STATS_{self.images[0].subject}_REML.nii.gz"

        if self.generate_residuals:
            self.rwherr = f"wherr_{self.images[0].subject}_REML.nii.gz"
            self.rerrts = f"errts_{self.images[0].subject}_REML.nii.gz"
        else:
            self.rwherr = None
            self.rerrts = None

        GLM.__init__(self,
                     images=self.images,
                     working_dir=self.working_dir,
                     glm_type=self.glm_type,
                     glm_label=self.glm_label,
                     input=self.input,
                     force_tr=self.force_tr,
                     hemisphere=self.hemisphere,
                     censor=self.censor,
                     polort=self.polort,
                     regressors_models_labels=self.regressors_models_labels,
                     ortvec=self.ortvec,
                     contrasts_labels=self.contrasts_labels,
                     roistats_designs_postfixes=self.roistats_designs_postfixes,
                     extension=self.extension)


        self.deconvolve = BashCommand.deconvolve(
            local_times=True,
            x1D_stop=True,
            GOFORIT=5,
            force_tr=None,
            input=self.generate_input(),
            polort=self.polort,
            float=True,
            censor=self.censor,
            regressors_models_labels=self.regressors_models_labels,
            ortvec=self.ortvec,
            x1D="X.xmat.1D",
            xjpeg="X.jpg",
            nobucket=True)

        self.remlfit = BashCommand.remlfit(
            matrix="X.xmat.1D",
            GOFORIT=5,
            input=self.input,
            contrasts_labels=self.contrasts_labels,
            Rvar=self.Rvar,
            Rbuck=self.Rbuck,
            rwherr=self.rwherr,
            rerrts=self.rerrts,
            fout=True,
            tout=True,
            nobout=True,
            verb=True)

        return

    def generate_input(self):
        input_arg = ""
        for image in self.images:
            scan = os.path.join(self.working_dir,
                                image.subject,
                                'INPUT_DATA',
                                image.task,
                                image.session,
                                image.afni_ready_volume_file)
            input_arg = f"{input_arg} {scan}"
        # " scan scan2 scan3"
        return input_arg.lstrip()


class SurfaceGLM(GLM):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        prop_defaults = {
            "images": None,
            "working_dir": None,
            "glm_type": "",
            "glm_label": "",
            "force_tr": '1.2',
            "polort": 'A',
            "hemisphere": None,
            "generate_residuals": False,
            "censor": "/path/to/censorFile",
            "regressors_models_labels": [],
            "ortvec": "/path/to/MovementFile",
            "contrasts_labels": [],
            "roistats_designs_postfixes": [],
            "extension": ".func.gii"
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.style = f"""Surface {self.hemisphere}"""
        self.results_dir = "1TRpK_SURFACE_RESULTS"
        self.Rvar = f"stats_var_{self.images[0].subject}_REML_{self.hemisphere}.func.gii"
        self.Rbuck = f"STATS_{self.images[0].subject}_REML_{self.hemisphere}.func.gii"

        if self.generate_residuals:
            self.rwherr = f"wherr_{self.images[0].subject}_REML_{self.hemisphere}.func.gii"
            self.rerrts = f"errts_{self.images[0].subject}_REML_{self.hemisphere}.func.gii"
        else:
            self.rwherr = None
            self.rerrts = None

        GLM.__init__(self,
                     images=self.images,
                     working_dir=self.working_dir,
                     glm_type=self.glm_type,
                     glm_label=self.glm_label,
                     input=self.generate_input(),
                     force_tr=self.force_tr,
                     hemisphere=self.hemisphere,
                     polort=self.polort,
                     censor=self.censor,
                     regressors_models_labels=self.regressors_models_labels,
                     ortvec=self.ortvec,
                     contrasts_labels=self.contrasts_labels,
                     roistats_designs_postfixes=self.roistats_designs_postfixes,
                     extension=self.extension)

        self.deconvolve = BashCommand.deconvolve(
            local_times=True,
            x1D_stop=True,
            GOFORIT=5,
            force_tr=self.force_tr,
            input=self.generate_input(),
            polort=self.polort,
            float=True,
            censor=self.censor,
            regressors_models_labels=self.regressors_models_labels,
            ortvec=self.ortvec,
            x1D=f"X.xmat_{self.hemisphere}.1D",
            xjpeg=f"X_{self.hemisphere}.jpg",
            nobucket=True)

        self.remlfit = BashCommand.remlfit(
            matrix=f"X.xmat_{self.hemisphere}.1D",
            GOFORIT=5,
            input=self.input,
            contrasts_labels=self.contrasts_labels,
            Rvar=self.Rvar,
            Rbuck=self.Rbuck,
            rwherr=self.rwherr,
            rerrts=self.rerrts,
            fout=True,
            tout=True,
            nobout=True,
            verb=True)

        return

    def generate_input(self):
        input_arg=""
        for image in self.images:
            scan = os.path.join(self.working_dir,
                                     image.subject,
                                     'INPUT_DATA',
                                     image.task,
                                     image.session,
                                     image.get_afni_ready_surface_file(self.hemisphere))
            input_arg=f"{input_arg} {scan}"
        #" scan scan2 scan3"
        return input_arg.lstrip()

