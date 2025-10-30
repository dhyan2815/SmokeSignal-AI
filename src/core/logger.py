import logging
from src.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(settings.app_name)
