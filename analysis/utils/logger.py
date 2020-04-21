import logging


def setup_logger(log_file, level=logging.DEBUG):
    log = logging.getLogger()  # root logger
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)


    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    log.setLevel(level)
    log.addHandler(fileHandler)
    log.addHandler(streamHandler)
    logging.root = logging.getLogger()

def logger(msg, level):
    if level == 'info': logging.info(msg)
    if level == 'warning': logging.warning(msg)
    if level == 'error': logging.error(msg)

