import logging


def setup_logger(logger_name, log_file, level=logging.DEBUG):
    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    log_setup.addHandler(streamHandler)
    logging.root = logging.getLogger(logger_name)

def logger(msg, level):
    if level == 'info': logging.info(msg)
    if level == 'warning': logging.warning(msg)
    if level == 'error': logging.error(msg)

