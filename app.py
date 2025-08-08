import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import utility modules
from alerts import send_email_alert
from preprocess import normalize_image, get_image_info, preprocess_for_model

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

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")
enable_alerts = st.sidebar.checkbox("Enable Email Alerts", value=False)

# Check email configuration status
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")
email_configured = bool(email_address and email_password)

if enable_alerts:
    if email_configured:
        st.sidebar.success("✅ Email alerts configured")
        st.sidebar.info("Email credentials loaded successfully")
        st.sidebar.info("Alerts will be sent when wildfires detected")
    else:
        st.sidebar.error("❌ Email not configured")
        st.sidebar.info("Please check your .env file")
        st.sidebar.info("Email alerts will not work")
else:
    st.sidebar.info("Email alerts disabled")

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
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.warning(f"🚨 Alert triggered at {now}")
                
                # Send email alert if enabled
                if enable_alerts:
                    if email_configured:
                        try:
                            send_email_alert(now, confidence_score)
                            st.success("📧 Email alert sent successfully!")
                        except Exception as e:
                            st.error(f"Failed to send email alert: {str(e)}")
                            st.info("Please check your email configuration")
                    else:
                        st.error("❌ Email alerts not configured")
                        st.info("Please set up your .env file with EMAIL_ADDRESS and EMAIL_PASSWORD")
            else:
                st.success("✅ Area appears to be safe from wildfires")
                
        except Exception as e:
            st.error("Prediction failed. Please check model and input format.")
            st.text(str(e))

# Add demo section
st.markdown("---")
st.header("📋 Demo Instructions")
st.markdown("""
### How to use SmokeSignal-AI:

1. **Upload an Image**: Use the file uploader above to select a satellite image
2. **Automatic Analysis**: The AI will analyze the image for wildfire indicators
3. **Results**: You'll see either:
   - 🔥 **Wildfire Detected** - with timestamp and optional email alert
   - ✅ **No Wildfire Detected** - indicating the area is safe
4. **Email Alerts**: Enable in sidebar to receive notifications for detected wildfires

### Supported Image Formats:
- JPG/JPEG
- PNG

### What the AI Detects:
- Smoke plumes
- Active fire areas
- Burn scars
- Thermal anomalies
""")

