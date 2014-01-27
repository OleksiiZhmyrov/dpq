import logging
import sys


def __setup_logging__(log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter("%(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

LOGGER = __setup_logging__()