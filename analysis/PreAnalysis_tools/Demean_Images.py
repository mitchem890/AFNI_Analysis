import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from classes import BashCommand


# Demean
def volume_demean_images_pipeline(image, fullpath):
    print(f'Running Volume Demean Images: {image.subject} {image.session} {image.task}')
    pipeline = []
    tmp_files = image.create_temporary_volume_files()

    pipeline.append(BashCommand.AutoMask(infile=os.path.join(fullpath, tmp_files['baseFilename']),
                                         outfile=os.path.join(fullpath, tmp_files['maskFilename'])))
    pipeline.append(BashCommand.BlurToFWHM(infile=os.path.join(fullpath, tmp_files['baseFilename']),
                                           outfile=os.path.join(fullpath, tmp_files['blurFilename'])))
    pipeline.append(BashCommand.Tstat(infile=os.path.join(fullpath, tmp_files['blurFilename']),
                                      outfile=os.path.join(fullpath, tmp_files['meanBlurFilename'])))
    pipeline.append(BashCommand.Calc(infile_a=os.path.join(fullpath, tmp_files['blurFilename']),
                                     infile_b=os.path.join(fullpath, tmp_files['meanBlurFilename']),
                                     outfile=os.path.join(fullpath, tmp_files['scaleBlurFilename'])))
    pipeline.append(BashCommand.Reorient(infile=os.path.join(fullpath, tmp_files['scaleBlurFilename']),
                                         outfile=os.path.join(fullpath, image.afni_ready_volume_file)))

    return pipeline


def surface_demean_pipeline(image, fullpath, hemisphere):
    pipeline = []
    tmp_files = image.create_temporary_surface_files(hemisphere=hemisphere)
    pipeline.append(BashCommand.Tstat(infile=os.path.join(fullpath, tmp_files['baseFilename']),
                                      outfile=os.path.join(fullpath, tmp_files['meanFilename'])))
    pipeline.append(BashCommand.Calc(infile_a=os.path.join(fullpath, tmp_files['baseFilename']),
                                     infile_b=os.path.join(fullpath, tmp_files['meanFilename']),
                                     outfile=os.path.join(fullpath, image.get_afni_ready_surface_file(hemisphere))))
    #pipeline.append(BashCommand.Reorient(infile=os.path.join(fullpath, tmp_files['scaleFilename']),
    #                                     outfile=os.path.join(fullpath, image.get_afni_ready_surface_file(hemisphere))))

    return pipeline


def cleanup(fullpath, tmp_files_dict):
    for key in tmp_files_dict:
        os.remove(os.path.join(fullpath, tmp_files_dict[key]))


def volume_demean_images(destination, images):
    for image in images:

        fullpath = os.path.join(destination, image.subject, 'INPUT_DATA', image.task, image.session)
        if not os.path.isfile(os.path.join(fullpath, image.afni_ready_volume_file)):
            for process in volume_demean_images_pipeline(image, fullpath):
                print(f"{process} of {image}")
                process.run_command()

            if os.path.isfile(os.path.join(fullpath, image.afni_ready_volume_file)):
                cleanup(fullpath, image.create_temporary_volume_files())
            else:
                print(f"There was an issue making lpi_scale_blur4 for {image} please Check")
        else:
            print(f"Previous version of lpi_scale_blur4 for {image} found, skipping")


def surface_demean_images(destination, hemisphere, images):
    for image in images:

        fullpath = os.path.join(destination, image.subject, 'INPUT_DATA', image.task, image.session)
        os.chdir(fullpath)
        if not os.path.isfile(os.path.join(fullpath, image.get_afni_ready_surface_file(hemisphere=hemisphere))):

            for process in surface_demean_pipeline(image, fullpath, hemisphere):
                print(f"{process} of {image}")
                process.run_command()

            if os.path.isfile(os.path.join(fullpath, image.get_afni_ready_surface_file(hemisphere=hemisphere))):
                cleanup(fullpath, image.create_temporary_surface_files(hemisphere=hemisphere))
            else:
                print(f"There was an issue making lpi_scale for {image} please Check")

        else:
            print(f"Previous version of lpi_scale for {image} found, skipping")
