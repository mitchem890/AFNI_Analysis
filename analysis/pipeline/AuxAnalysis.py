from classes.aux_code_thread import Thread
from utils import logger
from utils import RunShellFunc
import os
def create_logger(log_file):
    print(f"Creating log file")
    logger.setup_logger(log_file)

def aux_analysis(Thread: Thread, aux_analysis_dir):
    create_logger(os.path.join(aux_analysis_dir, Thread.log_file))
    print(f"Running {Thread.thread_name}")
    for script in Thread.scripts:
        RunShellFunc.run_shell_command(f"bash {os.path.join(aux_analysis_dir,script)}")