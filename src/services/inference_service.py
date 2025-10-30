import tensorflow as tf
from src.core.config import Config
from src.core.logger import setup_logger
import numpy as np

logger = setup_logger(__name__)

# Load model once at startup
try:
    model = tf.keras.models.load_model(Config.MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

def preprocess_image(image):
    # ✅ image is already a PIL Image
    img = image.resize((64, 64))
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)


async def predict_fire(image):
    if model is None:
        return {"error": "Model not loaded."}

    img_array = preprocess_image(image)
    prediction = model.predict(img_array)
    confidence = float(np.max(prediction))
    label = "Wildfire" if np.argmax(prediction) == 1 else "No Fire"
    return {"label": label, "confidence": confidence}
