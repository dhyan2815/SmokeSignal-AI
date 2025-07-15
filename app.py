import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import smtplib
import os
from datetime import datetime

# Load model
model = load_model("app/model/wildfire_detector_model.keras")

# Title and description
st.set_page_config(page_title="SmokeSignal-AI", layout="centered")
st.title("🔥 SmokeSignal-AI")
st.markdown("Upload a satellite image to detect **wildfires**.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Prediction
def predict(img):
    img = img.resize((150, 150))  # change to your model input size
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0
    preds = model.predict(x)
    return preds[0][0] > 0.5  # Adjust based on threshold

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    with st.spinner("Analyzing..."):
        result = predict(img)
        label = "🔥 Wildfire Detected" if result else "✅ No Wildfire"
        st.subheader(label)

        # Optional: send alert
        if result:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.warning(f"Alert triggered at {now}")
            # send_email_alert(now)

