import yaml



def build_threads(yaml_file):
    with open(yaml_file, 'r') as f:
        metadata = yaml.safe_load(f)

class thread(object):
    def __init__(self, thread_name: str, logger_name: str, shell_scripts: []):
        self.thread_name = thread_name
        self.logger_name = logger_name
        self.shell_scripts = shell_scripts
        return