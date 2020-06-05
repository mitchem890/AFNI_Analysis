import logging


def setup_logger(log_file, level=logging.DEBUG):
    log = logging.getLogger()  # root logger
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)


    logging.basicConfig(level=level, filename=log_file, filemode='w',
                        format='%(levelname)s: %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')  # Set the format of the log file name
    logging.root = logging.getLogger()

def logger(msg, level):
    if level == 'info': logging.info(msg)
    if level == 'warning': logging.warning(msg)
    if level == 'error': logging.error(msg)

