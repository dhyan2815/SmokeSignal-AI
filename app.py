import gradio as gr
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load the trained model
model = load_model("model/wildfire_detector_model.keras")

# Prediction function
def predict(img):
    img = img.resize((150, 150))  # your model input size
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0
    pred = model.predict(x)[0][0]
    label = "🔥 Wildfire Detected" if pred > 0.5 else "✅ No Wildfire"
    return label

# Gradio interface
iface = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="SmokeSignal-AI 🔥",
    description="Upload a satellite image to detect wildfires in real-time."
)

# Launch the app
if __name__ == "__main__":
    iface.launch()
