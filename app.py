import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
from datetime import datetime
import os
import sys

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import configuration and utility modules
from config import Config
from alerts import send_email_alert
from preprocess import get_image_info, preprocess_for_model

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
st.set_page_config(
    page_title="SmokeSignal AI",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.title("🔥 SmokeSignal AI")
st.markdown("""
    ### Wildfire Detection System
    """)
st.markdown("Upload a satellite image to detect **wildfires**.")

# Email alert configuration status (auto-enabled if configured)
email_configured = Config.is_email_configured()
enable_alerts = email_configured

if enable_alerts:
    st.info("Email alerts are enabled and will be sent when a wildfire is detected.")
else:
    st.warning("Email alerts not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD in your environment to enable alerts.")

# Add expandable instructions section
with st.expander("ℹ️ Click here for a quick guide on **How To Use** SmokeSignal AI", expanded=False):
    st.markdown("""
    #### **User Instructions**
    
    **Step 1: Upload Image**
    - Click "Browse files" below
    - Select any satellite/aerial image (JPG, PNG)
    - Image will be automatically processed
    
    **Step 2: System Analysis**
    - System analyzes image for wildfire indicators
    - Detects smoke plumes, fire areas, thermal signatures
    - Provides confidence score (0-100%)
    
    **Step 3: Results & Alerts**
    - **🔥 Wildfire Detected**: Shows confidence, timestamp, optional email alert
    - **✅ No Wildfire**: Confirms area is safe
    
    """)

# Sidebar removed; alerts are auto-enabled based on configuration

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Prediction function using utility preprocessing
def predict(img):
    # Get image information
    img_info = get_image_info(img)
    
    # Preprocess image for model
    x = preprocess_for_model(img, model.input_shape[1:])
    
    if x is None:
        raise Exception("Failed to preprocess image")
    
    # Get prediction and confidence score
    preds = model.predict(x)
    confidence_score = preds[0][0]
    result = confidence_score > 0.5
    
    return result, confidence_score, img_info

# If image uploaded
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_container_width=True)

    with st.spinner("Analyzing satellite image..."):
        try:
            result, confidence_score, img_info = predict(img)
            label = "🔥 Wildfire Detected" if result else "✅ No Wildfire Detected"
            st.subheader(label)

            if result:
                # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.warning("Initiating automated notification to designated emergency response contacts 🔔")
                
                # Send email alert if enabled and properly configured
                if enable_alerts:
                    try:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        send_email_alert(timestamp, confidence_score, img_info)
                        st.success("🔥 Wildfire Alert sent successfully via email 📧")
                    except Exception as e:
                        st.error(f"Failed to send email alert: {str(e)}")
                        st.info("Please check your email configuration")
                else:
                    st.error("❌ Email alerts not configured")
                    st.info("Set EMAIL_ADDRESS and EMAIL_PASSWORD in your environment to enable alerts")
            else:
                st.success("✅ Area appears to be safe from wildfires")
                
        except Exception as e:
            st.error("Prediction failed. Please check model and input format.")
            st.text(str(e))

