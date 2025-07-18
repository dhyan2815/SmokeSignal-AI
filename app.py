import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
from datetime import datetime
import os

# Load model
model = load_model("model/wildfire_detector_model.keras")

# Get model input size
input_shape = model.input_shape  # e.g., (None, 64, 64, 3) or (None, 12288)
if len(input_shape) == 4:
    img_height, img_width = input_shape[1], input_shape[2]
    flatten_input = False
elif len(input_shape) == 2:
    img_height = img_width = int((input_shape[1] // 3) ** 0.5)
    flatten_input = True
else:
    raise ValueError("Unsupported model input shape.")

# Streamlit UI
st.set_page_config(page_title="SmokeSignal-AI", layout="centered")
st.title("🔥 SmokeSignal-AI")
st.markdown("Upload a satellite image to detect **wildfires**.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Prediction function
def predict(img):
    img = img.resize((img_width, img_height))
    x = image.img_to_array(img)

    if flatten_input:
        x = x.reshape(1, -1)
    else:
        x = np.expand_dims(x, axis=0)

    x = x / 255.0
    preds = model.predict(x)
    return preds[0][0] > 0.5

# If image uploaded
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_container_width=True)

    with st.spinner("Analyzing..."):
        try:
            result = predict(img)
            label = "🔥 Wildfire Detected" if result else "✅ No Wildfire Detected"
            st.subheader(label)

            if result:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.warning(f"🚨 Alert triggered at {now}")
        except Exception as e:
            st.error("Prediction failed. Please check model and input format.")
            st.text(str(e))
