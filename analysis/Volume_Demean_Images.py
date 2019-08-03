import os
import RunShellFunc as rs
import time

def AutoMask(input, output):
    start = time.time()
    print("Running AutoMask")
    rs.run_shell_command('3dAutomask -dilate 1 -prefix ' + output + ' ' + input)
    end = time.time()
    print("time elapsed is " + str(end - start))

def BlurtoFWHM(input, output):
    if not os.path.isfile(output):
        start = time.time()
        print("Running BlurtoFWHM")
        rs.run_shell_command('3dBlurToFWHM -input ' + input + ' -prefix ' +output + ' -FWHM 4')
        end = time.time()
        print("time elapsed is " + str(end - start))
    else:
        print("Found a previous version of 3dBlured image")
def Tstat(input, output):
    if not os.path.isfile(output):
        start = time.time()
        print("Running Tstat")
        rs.run_shell_command('3dTstat -prefix ' + output + ' ' + input)
        end = time.time()
        print("time elapsed is " + str(end - start))
    else:
        print("Found a previous version of Tstat image")
def Calc(input_a, input_b,  output):
    if not os.path.isfile(output):

        start = time.time()
        print("Running 3dCalc")
        rs.run_shell_command('3dcalc  -a ' + input_a + ' -b ' + input_b +
                         " -expr 'min(200, a/b*100)*step(a)*step(b)'" +
                         ' -prefix ' + output)
        end = time.time()
        print("time elapsed is " + str(end - start))
    else:
        print("Found a previous version of Calc image")
def reorient(input, output):
    if not os.path.isfile(output):
        start = time.time()
        print("Running Reorient")
        rs.run_shell_command('3dresample -orient LPI'
                            ' -prefix ' + output +
                            ' -inset ' + input)
        end = time.time()
        print("time elapsed is" + str(end - start))
    else:
        print("Found a previous version of reorient image")

def volume_demean_images(destination, subject, session, task, runNum, encoding):
    print('Running Volume Demean')
    fullpath = os.path.join(destination, subject, 'INPUT_DATA', task, session)
    baseFilename='tfMRI_' + task.title() + session[0:3].title() + runNum + '_' + encoding + '.nii.gz'
    maskFilename='mask_' + baseFilename
    blurFilename='blur4_' + baseFilename
    meanBlurFilename='mean_' + blurFilename
    scaleBlurFilename='scale_' + blurFilename
    lpiScaleBlurFilename='lpi_' + scaleBlurFilename

    if not os.path.isfile(os.path.join(fullpath, lpiScaleBlurFilename)):

        AutoMask(os.path.join(fullpath, baseFilename), os.path.join(fullpath, maskFilename))

        BlurtoFWHM(os.path.join(fullpath, baseFilename), os.path.join(fullpath, blurFilename))

        Tstat(os.path.join(fullpath, blurFilename), os.path.join(fullpath, meanBlurFilename))

        Calc(input_a=os.path.join(fullpath,blurFilename),
            input_b=os.path.join(fullpath,meanBlurFilename),
            output=os.path.join(fullpath,scaleBlurFilename))

        reorient(input=os.path.join(fullpath, scaleBlurFilename),
                output=os.path.join(fullpath, lpiScaleBlurFilename))
    #TODO throw a big error if it doesnt exist
        if os.path.isfile(os.path.join(fullpath, lpiScaleBlurFilename)):
            os.remove(os.path.join(fullpath, baseFilename))
            os.remove(os.path.join(fullpath, maskFilename))
            os.remove(os.path.join(fullpath, blurFilename))
            os.remove(os.path.join(fullpath, meanBlurFilename))
            os.remove(os.path.join(fullpath, scaleBlurFilename))
    else:
        print("Found Previous version of the lpi_scale_blur4 Image skipping Demeaning image")