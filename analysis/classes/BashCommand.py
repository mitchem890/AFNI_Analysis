import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import globals
from utils import RunShellFunc as rs
from config import ConfigGLMs


# This fill contains the structure for all the bash
# commands that will be ran over the course of the processing
# Each bash command should a build_command function and a run_command function

#This is the General bash Command class. All bash commands will be Built off of this.
#If you use the parameter outfile in a subclass. The BashCommand class will check to see if the file already exists.
# If it does it will skip that processing step
class BashCommand(object):
    def __init__(self, command: str, return_output: bool):
        self.command = command
        self.return_output = return_output

    def run_command(self):
        if (not self.outfile_exist()) or (globals.overwrite):
            return rs.run_shell_command(self.command, return_output=self.return_output)
        else:
            print(f"Found previous {self.outfile} skipping")

    def outfile_exist(self):
        try:
            return os.path.isfile(self.outfile)
        except:
            return False


# This will build the 3dDeconvolve command used in the GLMs
# This assumes a format of:
# 3dDeconvolve \
# -local_times \
# -x1D_stop \
# -GOFORIT 5 \
# -input '/mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/lpi_scale_blur4_tfMRI_AxcptBas1_AP.nii.gz /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/lpi_scale_blur4_tfMRI_AxcptBas2_PA.nii.gz' \
# -polort A \
# -float \
# -censor /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/movregs_FD_mask.txt \
# -num_stimts 8 \
# -stim_times_AM1 1 /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/150423_Axcpt_baseline_block.txt 'dmBLOCK(1)' -stim_label 1 block \
# -stim_times 2 /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/150423_Axcpt_baseline_blockONandOFF.txt 'TENTzero(0,16.8,8)' -stim_label 2 blockONandOFF \
# -stim_times 3 /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/150423_Axcpt_baseline_AX.txt 'TENTzero(0,21.6,10)' -stim_label 3 AX \
# -stim_times 4 /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/150423_Axcpt_baseline_AY.txt 'TENTzero(0,21.6,10)' -stim_label 4 AY \
# -stim_times 5 /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/150423_Axcpt_baseline_Ang.txt 'TENTzero(0,21.6,10)' -stim_label 5 Ang \
# -stim_times 6 /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/150423_Axcpt_baseline_BX.txt 'TENTzero(0,21.6,10)' -stim_label 6 BX \
# -stim_times 7 /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/150423_Axcpt_baseline_BY.txt 'TENTzero(0,21.6,10)' -stim_label 7 BY \
# -stim_times 8 /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/150423_Axcpt_baseline_Bng.txt 'TENTzero(0,21.6,10)' -stim_label 8 Bng \
# -ortvec /mnt/LabWork/Afni_Analysis/150423/INPUT_DATA/Axcpt/baseline/motion_demean_baseline.1D movregs \
# -x1D X.xmat.1D \
# -xjpeg X.jpg \
# -nobucket"
#
# Where the First stim time will alway be an AM1 Block stim time you may want to alter this in the future
class Deconvolve(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "local_times": True,
            "x1D_stop": True,
            "GOFORIT": 5,
            "force_tr": None,
            "input": None,
            "polort": 'A',
            "float": True,
            "censor": None,
            "regressors_models_labels": [],
            "ortvec": None,
            "x1D": "X.xmat.1D",
            "xjpeg": "X.jpg",
            "nobucket": True
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        self.outfile = self.x1D
        BashCommand.__init__(self, command=self.command, return_output=False)

    def generate_force_tr(self):
        force_tr_parameter = ""
        if self.force_tr is not None:
            force_tr_parameter = f"\n-force_TR {self.force_tr} \\"
        return force_tr_parameter

    def generate_stim_times(self):

        if self.regressors_models_labels:

            stim_times = f"-num_stimts {str(len(self.regressors_models_labels))} \\\n"

            stim_times = stim_times + f"-stim_times_AM1 1 {self.regressors_models_labels[0][0]} {self.regressors_models_labels[0][1]} -stim_label 1 {self.regressors_models_labels[0][2]} \\\n"

            if len(self.regressors_models_labels) > 1:
                # Add in the variable amount of stim times with their labels models and file names
                for i in range(len(self.regressors_models_labels) - 1):
                    stim_times = stim_times + f"-stim_times {str(i + 2)} {self.regressors_models_labels[i + 1][0]} {self.regressors_models_labels[i + 1][1]} -stim_label {str(i + 2)} {self.regressors_models_labels[i + 1][2]} \\\n"

        return stim_times

    def build_command(self):
        command = f"""3dDeconvolve \\
-local_times \\
-x1D_stop \\
-GOFORIT {self.GOFORIT} \\{self.generate_force_tr()}
-input '{self.input}' \\
-polort {self.polort} \\
-float \\
-censor {self.censor} \\
{self.generate_stim_times()}-ortvec {self.ortvec} movregs \\
-x1D {self.x1D} \\
-xjpeg {self.xjpeg} \\
-nobucket"""

        return command


# This will build the 3dRemlfit command used in glms
class Remlfit(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "matrix": "X.xmat.1D",
            "GOFORIT": 5,
            "input": None,
            "contrasts_labels": [],
            "Rvar": None,
            "Rbuck": None,
            "rwherr": None,
            "rerrts": None,
            "fout": True,
            "tout": True,
            "nobout": True,
            "verb": True
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        self.outfile = self.Rbuck
        BashCommand.__init__(self, command=self.command, return_output=False)

    def generate_options(self):
        option_string = ""
        if self.rwherr:
            option_string = f"{option_string}-rwherr {self.rwherr} \\\n"
        if self.rerrts:
            option_string = f"{option_string}-rerrts {self.rerrts} \\\n"
        if self.fout:
            option_string = f"{option_string}-fout \\\n"
        if self.tout:
            option_string = f"{option_string}-tout \\\n"
        if self.nobout:
            option_string = f"{option_string}-nobout \\\n"
        if self.verb:
            option_string = f"{option_string}-verb \\\n"

        option_string = option_string.rstrip(" \\\n")
        return option_string

    def generate_contrasts(self):
        contrasts = ""
        if len(self.contrasts_labels) > 0:
            contrasts = "\n"

            for item in self.contrasts_labels:
                contrasts = f"{contrasts}-gltsym 'SYM: {item[0]}' {item[1]} \\\n"

        return contrasts[:-1]

    def build_command(self):
        command = f"""3dREMLfit \\
-matrix {self.matrix} \\
-GOFORIT {self.GOFORIT} \\
-input '{self.input}' \\{self.generate_contrasts()}
-Rvar {self.Rvar} \\
-Rbuck {self.Rbuck} \\
{self.generate_options()}"""
        return command


class Roistats(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "input": None,
            "name": None,
            "working_dir": None,
            "atlas": None,
            "extension": None,
            "subbrick": None,
            "outfile": None
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def build_command(self):
        command = f"""bash /home/analysis/BashScripts/Roistats.sh \\
-i {self.input} \\
-n {self.name} \\
-w {self.working_dir} \\
-a {self.atlas} \\
-r \"{self.extension}\" \\
-b {self.subbrick} \\
-f {self.outfile}"""
        return command


# This will take a movement regressors file in
# and write out a ecludian normalized text file out in the out file path
class ComputeEnorms(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "tr_count1": None,
            "tr_count2": None,
            "enormpath": None
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return f"Computing Enorms"

    def build_command(self):
        command = f"""1d_tool.py \\
-infile {self.infile} \\
-set_run_lengths {self.tr_count1} {self.tr_count2} \\
-derivative \\
-collapse_cols euclidean_norm \\
-write {self.enormpath} \\
-overwrite"""

        return command


# This will demean the motion parameters in the output file
class DemeanMotionParameters(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "tr_count1": None,
            "tr_count2": None,
            "demeanpath": None
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return f"Demeaning Motion Parameters"

    def build_command(self):
        command = f"""1d_tool.py 
-infile { self.infile } \\
-set_run_lengths {self.tr_count1} {self.tr_count2} \\
-demean \\
-write {self.demeanpath} \\
-overwrite"""
        return command


class ComputeMotionParameterDerivatives(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "tr_count1": None,
            "tr_count2": None,
            "derivpath": None
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return "Computing Motion Parameter Derivatives"

    def build_command(self):
        command = f"""1d_tool.py 
-infile {self.infile} \\
-set_run_lengths {self.tr_count1} {self.tr_count2} \\
-derivative \\
-demean \\
-write {self.derivpath} \\
-overwrite"""
        return command


class CreateCensorList(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "tr_count1": None,
            "tr_count2": None,
            "censor_list_file": None,
            "censorTR_file": None
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return f"Creating Censor List"

    def build_command(self):
        command = f"""1d_tool.py \\
-infile {self.infile} \\
-set_run_lengths {self.tr_count1} {self.tr_count2} \\
-derivative \\
-censor_prev_TR \\
-collapse_cols euclidean_norm \\
-moderate_mask -0.3 0.3 \\
-write {self.censor_list_file} \\
-write_CENSORTR {self.censorTR_file} \\
-verb 0 \\
-overwrite"""
        return command


class GetTRCount(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=True)

    def __str__(self):
        return f"Getting TR Count"

    def build_command(self):
        command = f"""3dinfo -nv {self.infile}"""
        return command

class GetTR(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=True)

    def __str__(self):
        return f"Getting TR"

    def build_command(self):
        command = f"""3dinfo -tr {self.infile}"""
        return command

class GetVoxelDimensions(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "dimension": 'i'
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=True)

    def __str__(self):
        return f"Getting Voxel dimensions"

    def build_command(self):
        command = f"""3dinfo -d{self.dimension} {self.infile}"""
        return command

class GetImageDimensions(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "dimension": 'i'
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=True)

    def __str__(self):
        return f"Getting image dimensions"

    def build_command(self):
        command = f"""3dinfo -n{self.dimension} {self.infile}"""
        return command


# Used to split Ciftis into left and right hemisphere Giftis
class CiftiSplit(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "outfile": None,
            "metric": None,
            "direction": "COLUMN"
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return f"Splitting Cifti Image: {self.metric}"

    def build_command(self):
        command = f"""wb_command \\
-cifti-separate {self.infile} {self.direction} -metric {self.metric} {self.outfile}"""
        return command


class CalculateFD(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "outfile": None
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return "Calculating FD's"

    def build_command(self):
        command = f"""bash /home/analysis/BashScripts/calculate_framewise_displacement.sh \\
{self.infile} \\
{self.outfile}"""
        return command


# This will run nicholases DVar calculating script on the input nifti image.
# it will create a text file in the outfile location
class CalculateDVars(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "outfile": None
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return f"Calculating Dvars"

    def build_command(self):
        command = f"""bash /home/analysis/BashScripts/dvars_nichols.sh {self.infile} {self.outfile}"""
        return command


# This will return a string of filter out frames for input images.
# with 1 for included frames and 0 for excluded frames
class MakeFDMask(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "expr": "within(a,0,0.9)"
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=True)

    def __str__(self):
        return f"Making Functional Displacement Mask"

    def build_command(self):
        command = f"""1deval \\
-expr '{self.expr}' \\
-a {self.infile}"""
        return command


# use 3dResample to resize volumetric images.
# you would normally use this to make an image fit to an atlas
class Resample(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "voxel_dim": None,
            "infile": None,
            "outfile": None
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        #Set the correct atlas for the MB of the image MB4 is 2p4 MB8 is 2.0
        if self.voxel_dim == '2.400000x2.400000x2.400000':
            self.atlas = os.path.join(ConfigGLMs.Atlas_Dir, "gordon_2p4_resampled_wsubcort_LPI.nii.gz")
        elif self.voxel_dim == '2.000000x2.000000x2.000000':
            self.atlas = os.path.join(ConfigGLMs.Atlas_Dir, "gordon_222_resampled_wsubcort_LPI.nii.gz")
        else:
            raise Exception("Could not get atlas for voxel dimensions")
        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return "Running 3dResample"

    def build_command(self):
        command = f"""3dresample \\
-master {self.atlas} \\
-input {self.infile} \\
-prefix {self.outfile}"""
        return command


class AutoMask(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "dilate": "1",
            "infile": None,
            "outfile": None
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return "Running AutoMask"

    def build_command(self):
        command = f"""3dAutomask 
-dilate {self.dilate} \\
-prefix {self.outfile} \\
{self.infile}"""
        return command


class BlurToFWHM(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "FWMH": "4",
            "infile": None,
            "outfile": None
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return "Running BlurToFWHM"

    def build_command(self):
        command = f"""3dBlurToFWHM \\
-input {self.infile} \\
-prefix {self.outfile} \\
-FWHM {self.FWMH}"""
        return command


class Tstat(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile": None,
            "outfile": None
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return "Running Tstat"

    def build_command(self):
        command = f"""3dTstat \\
-prefix {self.outfile} {self.infile}"""
        return command


#Runs calculation on the two input images
class Calc(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "infile_a": None,
            "infile_b": None,
            "expr": 'min(200, a/b*100)*step(a)*step(b)',
            "outfile": None
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return "Running 3dCalc"

    def build_command(self):
        command = f"""3dcalc \\
-a {self.infile_a} \\
-b {self.infile_b} \\
-expr '{self.expr}' \\
-prefix {self.outfile}"""
        return command


#Reorients The image to given orientation Default is LPI
class Reorient(BashCommand):
    def __init__(self, **kwargs):
        prop_defaults = {
            "orient": 'LPI',
            "infile": None,
            "outfile": None,
            "skip_reorient": False
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.command = self.build_command()
        BashCommand.__init__(self, command=self.command, return_output=False)

    def __str__(self):
        return "Running 3dReorient"

    def build_command(self):
        command = f"""3dresample \\
-orient {self.orient} \\
-prefix {self.outfile} \\
-inset {self.infile}"""
        return command
