import numpy as np
from PIL import Image
import tensorflow as tf
from src.core.logger import logger
from src.core.dependencies import get_model

def preprocess_image(image):
    """
    Preprocess a PIL image for the model.
    - Resize to (224, 224)
    - Normalize pixel values (0–1)
    - Add batch dimension
    """
    img = image.resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)  # shape: (1, 224, 224, 3)
    return arr

def run_inference(image):
    """
    Perform prediction using the globally loaded TensorFlow model.
    """
    try:
        model = get_model()  # ✅ model loaded once and cached
        if model is None:
            logger.error("Model not loaded — get_model() returned None.")
            return {"error": "Model not loaded."}

        img_array = preprocess_image(image)
        prediction = model.predict(img_array)

        confidence = float(np.max(prediction))
        label = "Wildfire" if np.argmax(prediction) == 1 else "No Fire"

        logger.info(f"Prediction: {label} ({confidence:.2f})")
        return {"label": label, "confidence": confidence}

    except Exception as e:
        logger.error(f"Inference error: {e}")
        return {"error": str(e)}
