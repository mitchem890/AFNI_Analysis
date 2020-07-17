import subprocess
import shlex
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from utils import logger
from config import globals


def load_user_parameters(env):
    env['origin'] = globals.origin
    env['subjects'] = globals.subjects
    env['wave'] = globals.wave
    env['tasks'] = globals.tasks
    env['sessions'] = globals.sessions
    env['destination'] = globals.destination
    env['events'] = globals.events
    env['run_volume'] = globals.run_volume
    env['run_surface'] = globals.run_surface
    env['run_analysis'] = globals.run_analysis
    env['run_preanalysis'] = globals.run_preanalysis
    env['pipeline'] = globals.pipeline
    env['ncpus'] = globals.ncpus
    env['aux_analysis'] = globals.aux_analysis
    return env
def run_shell_command(command_line, return_output=False):
    logger.logger(f'\nSubprocess: "{command_line}"', 'info')
    command_line = command_line.replace('\n', '')
    command_line_args = shlex.split(command_line)
    try:
        # This is container relative
        os.environ["PATH"] = '/opt/afni-latest' + os.pathsep \
                             + '/usr/lib' + os.pathsep + '/usr/bin' + os.pathsep + os.environ["PATH"]

        my_env = os.environ.copy()
        my_env['LD_LIBRARY_PATH'] = '/usr/lib'
        my_env = load_user_parameters(my_env)
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=my_env
        )

        process_output, _ = command_line_process.communicate()
        command_line_process.wait()
        # process_output is now a string, not a file,
        # you may want to do:
        # process_output = StringIO(process_output)
        process_output = clean_output(str(process_output))

        logger.logger(process_output, 'info')
        if command_line_process.returncode != 0:
            logger.logger(f'An Error Occured, Execption Code: {str(command_line_process.returncode)}', 'error')
            logger.logger('Subprocess failed', 'warning')
            return False

    except (OSError, subprocess.CalledProcessError) as exception:
        print("There was an Issue")
        logger.logger(f'Exception occured: {str(exception)}', 'error')
        logger.logger('Subprocess failed', 'error')
        return False

    # no exception was raised
    logger.logger('Subprocess finished\n', 'info')
    #TODO issue here will not return float
    if return_output:
        #Only return digits and decimals
        output = ''.join(c for c in str(process_output) if (c.isdigit() or c == '.'))
        return output

    return True


# Remove the the errors the waring from the textfile output
def clean_output(output):
    warning = 'has coordsys with intent NIFTI_INTENT_TIME_SERIES (should be NIFTI_INTENT_POINTSET)'
    return output.replace(warning, '')
