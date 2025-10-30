import logging
from src.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def setup_logger(name: str):
    """
    Sets up and returns a named logger
    """
    return logging.getLogger(name)

logger = logging.getLogger(settings.app_name)
