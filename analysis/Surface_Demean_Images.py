import os
import RunShellFunc as rs


def AutoMask(input, output):
    rs.run_shell_command('3dAutomask -dilate 1 -prefix ' + output + ' ' + input)


def BlurtoFWHM(input, output):
    rs.run_shell_command('3dBlurToFWHM -input ' + input + ' -prefix ' +output + ' -FWHM 4')


def Tstat(input, output):
    if not os.path.isfile(output):
        print("Running Tstat")
        rs.run_shell_command('3dTstat -prefix ' + output + ' ' + input)
    else:
        print("Found an previously created version of a tstat image")

def Calc(input_a, input_b,  output):
    if not os.path.isfile(output):
        print("Running Calc")
        rs.run_shell_command('3dcalc  -a ' + input_a + ' -b ' + input_b +
                             " -expr 'min(200, a/b*100)*step(a)*step(b)'" +
                             ' -prefix ' + output)
    else:
        print("Found an previously created version of a 3dCalc image")


def reorient(input, output):
    if not os.path.isfile(output):
        print("Running Reorient")
        rs.run_shell_command('3dresample -orient LPI'
                             ' -prefix ' + output +
                             ' -inset ' + input)
    else:
        print("Found an previously created version of a reoriented image")

def surface_demean_images(destination, subject, session, task, runNum, encoding, hemisphere):
    print('Running Surface Demean')
    fullpath = os.path.join(destination, subject, 'INPUT_DATA', task, session)
    baseFilename='tfMRI_' + task.title() + session[0:3].title() + runNum + '_' + encoding + '_'+hemisphere+'.func.gii'
    meanFilename='mean_' + baseFilename
    scaleFilename='scale_' + baseFilename
    lpiScaleFilename='lpi_' + scaleFilename
    os.chdir(fullpath)
    if not os.path.isfile(os.path.join(fullpath, lpiScaleFilename)):

        Tstat(os.path.join(fullpath, baseFilename), os.path.join(fullpath, meanFilename))
        Calc(input_a=os.path.join(fullpath, baseFilename),
             input_b=os.path.join(fullpath, meanFilename),
             output=os.path.join(fullpath, scaleFilename))

        reorient(input=os.path.join(fullpath, scaleFilename),
                 output=os.path.join(fullpath, lpiScaleFilename))

        if os.path.isfile(os.path.join(fullpath, lpiScaleFilename)):
            os.remove(os.path.join(fullpath, baseFilename))
            os.remove(os.path.join(fullpath, meanFilename))
            os.remove(os.path.join(fullpath, scaleFilename))
    else:
        print("Found Previous version of the lpi_scale Image skipping Demeaning image")
