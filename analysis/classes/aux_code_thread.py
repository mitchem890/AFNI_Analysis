import yaml


def load_yaml(yaml_file):
    with open(yaml_file, 'r') as f:
        dataMap = yaml.safe_load(f)
    return dataMap


class Thread(object):
    def __init__(self, thread_name: str, log_file: str, scripts: []):
        self.thread_name = thread_name
        self.log_file = log_file
        self.scripts = scripts
        return


def parse_dataMap(dataMap):
    threadsMap=dataMap.get("threads")
    Threads = []
    for threadMap in threadsMap:
        Threads.append(Thread(thread_name=threadMap.get("thread_name"), log_file=threadMap.get("log_file"), scripts=threadMap.get("scripts")))
    return Threads


def build_threads_from_yaml(yaml_file):
    dataMap = load_yaml(yaml_file=yaml_file)
    Threads = parse_dataMap(dataMap)
    return Threads
