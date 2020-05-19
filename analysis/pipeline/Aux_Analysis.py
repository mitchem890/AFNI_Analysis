from classes import aux_code_thread
from utils import logger
from utils import RunShellFunc

def create_logger(log_file):
    logger.setup_logger(log_file)

def aux_analysis(Thread: Thread):
    create_logger(Thread.log_file)
    print(f"Running {Thread.thread_name}")
    for script in Thread.scripts:
        RunShellFunc.run_shell_command(f"bash {script}")