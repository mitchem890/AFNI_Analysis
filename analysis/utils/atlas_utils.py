import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import ConfigGLMs
#This will retrun the correct set of atlases for a sitiuation
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

#This will return the correct extension to tack onto the atlases. This is used becuase the gordon has a different extension tha the rest of the atlases
def get_extension(atlas, hemisphere):
    if hemisphere is None:
        extension = '.nii.gz'
    elif atlas is "gordon_333":
        extension = ".func.gii"
    else:
        extension = ".label.gii"
    return extension