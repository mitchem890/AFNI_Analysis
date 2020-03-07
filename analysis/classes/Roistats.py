import os
import sys
from abc import ABCMeta

sys.path.append(os.path.abspath("/home/"))
from classes import BashCommand
from utils import atlas_utils
from config import ConfigGLMs



class roistats(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        prop_defaults = {
            "input_file": "path/to/scan1 /path/to/scan2",
            "design": None,
            "working_dir": None,
            "atlas": "",
            "session": None,
            "subject": None,
            "extension": None,
            "hemisphere": None,
            "postfix": None,
            "subbrick": None
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.outfile = self.generate_outfile()
        self.roistats = self.generate_command()


    def generate_outfile(self):
        atlas_file=os.path.basename(self.atlas)
        return f"{self.subject}_timecourses_{self.session}_{self.design}_{self.subbrick}{self.postfix}_{atlas_file}.txt"

    def generate_command(self):
        command = BashCommand.roistats(input=self.input_file,
                                       name=self.design,
                                       working_dir=self.working_dir,
                                       atlas=self.atlas,
                                       extension=self.extension,
                                       subbrick=self.subbrick,
                                       outfile=self.outfile)
        return command


# This will add the take the standard inputs
# to the roistats minus the atlas and extension
# it will return a list of roistats objects, one for each atlas available
def build_roistats(input_file='',
                   design='',
                   working_dir='',
                   session='',
                   subject='',
                   mb='',
                   hemisphere=None,
                   postfix=None,
                   fsaverage=True):
    roistats_list = []
    atlases_dir = ConfigGLMs.Atlas_Dir
    atlases = atlas_utils.get_correct_atlases(mb=mb, hemisphere=hemisphere, fsaverage=fsaverage)
    for atlas in atlases:

        extension = atlas_utils.get_extension(atlas, hemisphere)

        if hemisphere:
            atlas = f"{atlas}_{hemisphere}"
        Coef_roistat=roistats(
            input_file=input_file,
            design=design,
            working_dir=working_dir,
            atlas=os.path.join(atlases_dir, atlas),
            session=session,
            subject=subject,
            extension=extension,
            hemisphere=hemisphere,
            postfix=postfix,
            subbrick="Coef")
        Tstat_roistat=roistats(
            input_file=input_file,
            design=design,
            working_dir=working_dir,
            atlas=os.path.join(atlases_dir, atlas),
            session=session,
            subject=subject,
            extension=extension,
            hemisphere=hemisphere,
            postfix=postfix,
            subbrick="Tstat")
        roistats_list.extend([Coef_roistat, Tstat_roistat])

    return roistats_list

