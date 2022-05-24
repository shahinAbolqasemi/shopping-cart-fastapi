import logging
from logging import getLogger


def get_logger(name, level=logging.DEBUG, fmt: str = None):
    log_format = fmt or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(log_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
