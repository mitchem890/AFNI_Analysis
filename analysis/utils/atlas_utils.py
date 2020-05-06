import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import ConfigGLMs


#This will retrun the correct set of atlases for a sitiuation
def get_correct_atlases(image_dim, hemisphere, fsaverage):
    if hemisphere is None:
        if image_dim == '75x90x75':
            atlases = ConfigGLMs.VolumeAtlases2p4
        elif image_dim == '91x109x91':
            atlases = ConfigGLMs.VolumeAtlases222
    else:
        if image_dim == '75x90x75':
            atlases = ConfigGLMs.SurfaceAtlases2p4
        elif image_dim == '91x109x91':
            atlases = ConfigGLMs.SurfaceAtlases222
        if fsaverage:
            atlases = ConfigGLMs.SurfaceAtlasesFS5
    print(image_dim)
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