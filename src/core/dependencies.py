import tensorflow as tf
from functools import lru_cache
from src.core.config import settings
from src.core.logger import logger

@lru_cache()
def get_model():
    """
    Lazily load and cache the TensorFlow model once.
    """
    try:
        model = tf.keras.models.load_model(settings.MODEL_PATH)
        logger.info("✅ TensorFlow model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"❌ Failed to load TensorFlow model: {e}")
        return None
