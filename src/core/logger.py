import logging
from .config import Config

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)

    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s: %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
