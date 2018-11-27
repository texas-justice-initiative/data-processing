import logging


def set_up_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
