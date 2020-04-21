import logger
import subprocess
import shlex
import os



def run_shell_command(command_line, return_output=False):
    logger.logger(f'\nSubprocess: "{command_line}"')
    command_line = command_line.replace('\n', '')
    command_line_args = shlex.split(command_line)
    try:
        # This is container relative
        os.environ["PATH"] = '/opt/afni-latest' + os.pathsep \
                             + '/usr/lib' + os.pathsep + '/opt/workbench/bin_linux64' + os.pathsep + os.environ["PATH"]

        my_env = os.environ.copy()
        my_env['LD_LIBRARY_PATH'] = '/usr/lib'

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

    if return_output:
        output = ''.join(c for c in str(process_output) if c.isdigit())
        return output

    return True


# Remove the the errors the waring from the textfile output
def clean_output(output):
    warning = 'has coordsys with intent NIFTI_INTENT_TIME_SERIES (should be NIFTI_INTENT_POINTSET)'
    return output.replace(warning, '')
