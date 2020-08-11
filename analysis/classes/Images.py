import os
import glob
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from classes import BashCommand

# This File defines the image class, which stores data about found images

# Find Fmriprep images using pattern matching
def get_fmriprep_images(origin, wave, subject, session, task, pipeline):
    images = []
    origin = os.path.join(origin, f"sub-{str(subject)}", f"ses-{wave}{session[0:3].lower()}", "func")

    files = glob.glob(os.path.join(origin,
                                   f'sub-{subject}_ses-{wave}{session[0:3].lower()}_task-{task.title()}_acq-mb???_run-?_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'))

    for file in files:
        images.append(fmriprep_preprocessed_image(file, wave, subject, session, task, pipeline))
    return images


# fing HCP images using pattern matching
def get_hcp_images(origin, wave, subject, session, task, pipeline):
    images = []
    origin = os.path.join(origin, subject, 'MNINonLinear', 'Results', f"tfMRI_{task}{session[0:3].title()}?_??")
    files = glob.glob(os.path.join(origin, f"tfMRI_{task}{session[0:3].title()}?_??.nii.gz"))

    for file in files:
        images.append(hcp_preprocessed_image(file, wave, subject, session, task, pipeline))

    return images


def get_images(origin, wave, subject, session, task, pipeline):
    images = []

    if pipeline == 'fmriprep':
        images = get_fmriprep_images(origin, wave, subject, session, task, pipeline)
    elif pipeline == 'hcp':
        images = get_hcp_images(origin, wave, subject, session, task, pipeline)

    # resort the images by run number
    images.sort(key=lambda x: int(x.run_num), reverse=False)

    return images


class preprocessed_image(object):
    def __init__(self, file, wave, subject, session, task, pipeline, testMode = False):
        self.file = file
        self.wave = wave
        self.subject = subject
        self.session = session
        self.task = task
        self.pipeline = pipeline
        self.run_num = self.get_run_num()
        self.encoding = self.get_encoding()
        self.extension = self.get_extension()
        self.basename = self.get_basename()
        self.dirname = self.get_dirname()
        self.root_name = self.get_root_name()
        self.afni_ready_volume_file = self.get_afni_ready_volume_file()
        self.movement_regressor = self.get_movement_regessors_file()
        ##These three make it difficult to run a unit test on machine without an image Mybe think about setting fake value defaults
        if not testMode:
            self.tr = round(float(self.get_tr()), 2)
            self.set_voxel_dim(self.file)
            self.set_image_dim(self.file)
        else:
            self.tr = round(float('1.2'), 2)
            self.voxel_dim = '2.4000x2.400000x2.400000'
            self.image_dim = '75x90x75'

    def __str__(self):
        return f"{self.subject} {self.session} {self.task} {self.encoding}"

    # These are the files that will be created in the process of making the afni_ready_volume_file
    def create_temporary_volume_files(self):
        return {"baseFilename": f'tfMRI_{self.root_name}.nii.gz',
                "maskFilename": f'mask_tfMRI_{self.root_name}.nii.gz',
                "blurFilename": f'blur4_tfMRI_{self.root_name}.nii.gz',
                "meanBlurFilename": f'mean_blur4_tfMRI_{self.root_name}.nii.gz',
                "scaleBlurFilename": f'scale_blur4_tfMRI_{self.root_name}.nii.gz'}

    def create_temporary_surface_files(self, hemisphere):
        return {"baseFilename": f'tfMRI_{self.root_name}_{hemisphere}.func.gii',
                "meanFilename": f'mean_tfMRI_{self.root_name}_{hemisphere}.func.gii',
                }
        #"scaleFilename": f'scale_tfMRI_{self.root_name}_{hemisphere}.func.gii'

    def get_afni_ready_volume_file(self):
        return f'lpi_scale_blur4_tfMRI_{self.root_name}.nii.gz'

    def get_afni_ready_surface_file(self, hemisphere):
        return f"lpi_scale_tfMRI_{self.root_name}_{hemisphere}.func.gii"

    def get_root_name(self):
        return f"{self.task}{self.session[0:3].title()}{self.run_num}_{self.encoding}"

    def get_movement_regessors_file(self):
        return f"Movement_Regressors_{self.root_name}.txt"

    def get_regressor_files(self):
        self.hcp_fd = f"{self.subject}_tfMRI_{self.root_name}_FD.txt"
        self.hcp_dvars = f"{self.subject}_tfMRI_{self.root_name}_DVARS.txt"
        self.hcp_fd_mask = f"{self.subject}_tfMRI_{self.root_name}_FD_mask.txt"

    def get_tr(self):
        return BashCommand.get_tr(infile=self.file).run_command()

    def get_voxel_dim(self, file):
        dimensions_i = BashCommand.get_voxel_dimensions(infile=file, dimension='i').run_command()
        dimensions_j = BashCommand.get_voxel_dimensions(infile=file, dimension='j').run_command()
        dimensions_k = BashCommand.get_voxel_dimensions(infile=file, dimension='k').run_command()
        dimensions = f"{dimensions_i}x{dimensions_j}x{dimensions_k}".replace('-', '')
        return dimensions

    def get_image_dim(self, file):
        dimensions_i = BashCommand.get_image_dimensions(infile=file, dimension='i').run_command()
        dimensions_j = BashCommand.get_image_dimensions(infile=file, dimension='j').run_command()
        dimensions_k = BashCommand.get_image_dimensions(infile=file, dimension='k').run_command()
        dimensions = f"{dimensions_i}x{dimensions_j}x{dimensions_k}".replace('-', '')
        return dimensions

    def set_image_dim(self, file):
        self.image_dim = self.get_image_dim(file)

    def set_voxel_dim(self, file):
        self.voxel_dim = self.get_voxel_dim(file)


class fmriprep_preprocessed_image(preprocessed_image):
    def __init__(self, file, wave, subject, session, task, pipeline, testMode = False):
        self.fsaverage = True
        preprocessed_image.__init__(self, file, wave, subject, session, task, pipeline, testMode=testMode)
        self.fmriprep_root_name = f"sub-{str(self.subject)}_ses-{str(self.wave)}{str(self.session).lower()[0:3]}_task-{str(self.task)}_acq-mb4{str(self.encoding)}_run-{str(self.run_num)}"
        self.fmriprep_regressors = f"{self.fmriprep_root_name}_desc-confounds_regressors.tsv"

    def fmriprep_hcp_name_mapping(self):
        return {f"{self.fmriprep_root_name}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz": f"tfMRI_{self.root_name}.nii.gz",
                f"{self.fmriprep_root_name}_space-fsaverage5_hemi-L.func.gii": f"tfMRI_{self.root_name}_L.func.gii",
                f"{self.fmriprep_root_name}_space-fsaverage5_hemi-R.func.gii": f"tfMRI_{self.root_name}_R.func.gii"}


    def get_run_num(self):
        return os.path.basename(self.file).split('run-')[1][0]

    def get_encoding(self):
        return os.path.basename(self.file).split('mb')[1][1:3]

    def get_extension(self):
        return os.path.basename(self.file).split('.', 1)[1]

    def get_basename(self):
        return os.path.basename(self.file)

    def get_dirname(self):
        return os.path.dirname(self.file)


class hcp_preprocessed_image(preprocessed_image):
    def __init__(self, file, wave, subject, session, task, pipeline, testMode = False):
        self.fsaverage = False
        preprocessed_image.__init__(self, file, wave, subject, session, task, pipeline, testMode = testMode)

    def get_run_num(self):
        return os.path.basename(self.file).split('.', 1)[0][-4]

    def get_encoding(self):
        return os.path.basename(self.file).split('.', 1)[0][-2:]

    def get_extension(self):
        return os.path.basename(self.file).split('.', 1)[1]

    def get_basename(self):
        return os.path.basename(self.file)

    def get_dirname(self):
        return os.path.dirname(self.file)
