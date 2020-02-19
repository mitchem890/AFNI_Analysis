import os
from abc import ABCMeta

from classes import BashCommand
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
            "postfix": None
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.roistats = self.generate_command()

    def generate_command(self):
        command = BashCommand.roistats(input=self.input_file,
                                       name=self.design,
                                       working_dir=self.working_dir,
                                       atlas=self.atlas,
                                       session=self.session,
                                       subject=self.subject,
                                       extension=self.extension,
                                       model=self.postfix)
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
    atlases = get_correct_atlases(mb=mb, hemisphere=hemisphere, fsaverage=fsaverage)
    for atlas in atlases:

        extension = get_extension(atlas, hemisphere)

        if hemisphere:
            atlas = f"{atlas}_{hemisphere}"

        roistats_list.append(roistats(
            input_file=input_file,
            design=design,
            working_dir=working_dir,
            atlas=os.path.join(atlases_dir, atlas),
            session=session,
            subject=subject,
            extension=extension,
            hemisphere=hemisphere,
            postfix=postfix))

    return roistats_list


def get_correct_atlases(mb, hemisphere, fsaverage):
    if hemisphere is None:
        if mb is '4':
            atlases = ConfigGLMs.VolumeAtlasesMB4
        elif mb is '8':
            atlases = ConfigGLMs.VolumeAtlasesMB8
    else:
        if mb is '4':
            atlases = ConfigGLMs.SurfaceAtlasesMB4
        elif mb is '8':
            atlases = ConfigGLMs.SurfaceAtlasesMB8
        if fsaverage:
            atlases = ConfigGLMs.SurfaceAtlasesFS5

    return atlases


def get_extension(atlas, hemisphere):
    if hemisphere is None:
        extension = '.nii.gz'
    elif atlas is "gordon_333":
        extension = ".func.gii"
    else:
        extension = ".label.gii"
    return extension
