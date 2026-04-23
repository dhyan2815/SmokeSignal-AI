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
from ood import is_ood

# Load model
model = load_model("model/wildfire_detector_model.keras")

# Get model input size
input_shape = model.input_shape
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
st.markdown("Upload a image to detect **wildfires**.")

# Email alert configuration status
email_configured = Config.is_email_configured()
enable_alerts = email_configured

if enable_alerts:
    st.info("Email alerts are enabled and will be sent when a wildfire is detected.")
else:
    st.warning("Email alerts not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD in your environment to enable alerts.")

# Add expandable instructions section
with st.expander("ℹ️ Click here for a quick guide on **How To Use** SmokeSignal AI", expanded=False):
    st.markdown("""
    **Purpose**: Analyze aerial/satellite images for wildfire indicators.

    **How to use**
    1. Upload a JPG/PNG image.
    2. The system analyzes it automatically.
    3. Review the result:
       - 🔥 Wildfire Detected — with confidence
       - ✅ No Wildfire Detected

    **Alerts**
    - If email is configured, an alert is sent automatically when a wildfire is detected.

    **Note**
    - Results are AI-generated for decision support. Confirm with local authorities for emergencies.
    """)

# Prediction function using utility preprocessing
def predict(img):
    img_info = get_image_info(img)
    x = preprocess_for_model(img, model.input_shape[1:])
    
    if x is None:
        raise Exception("Failed to preprocess image")
    
    preds = model.predict(x)
    confidence_score = float(preds[0][0])
    result = confidence_score > 0.5
    
    return result, confidence_score, img_info

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# If image uploaded
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_container_width=True)

    # 1. Backend OOD Check
    with st.status("Performing backend distribution check...", expanded=False) as status:
        st.write("Analyzing image scene type...")
        is_flagged, scene_type, ood_conf = is_ood(img)
        
        if is_flagged:
            status.update(label="⚠️ Distribution Mismatch Detected", state="error", expanded=True)
            st.warning(f"Detected Scene: **{scene_type.title()}**")
            st.error("SmokeSignal AI is optimized for satellite/aerial imagery. The uploaded image appears to be out-of-distribution (OOD).")
            
            # Log OOD event to console instead of saving image
            print(f"[OOD LOG] {datetime.now()} - Flagged OOD Image: {scene_type} (Conf: {ood_conf:.2%})")
            st.stop()
        else:
            status.update(label="✅ Distribution Check Passed", state="complete")
            st.write(f"Validated Scene: {scene_type.title()} ({ood_conf:.1%})")

    # 2. Main Wildfire Detection
    with st.spinner("Analyzing satellite image..."):
        try:
            result, confidence_score, img_info = predict(img)
            label = "🔥 Wildfire Detected" if result else "✅ No Wildfire Detected"
            st.subheader(label)
            st.write(f"**Confidence Score:** {confidence_score:.2%}")

            if result:
                alert_status = st.empty()
                alert_status.warning("Initiating automated notification to emergency contacts 🔔")
                
                if enable_alerts:
                    try:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        send_email_alert(timestamp, confidence_score, img_info)
                        alert_status.success("🔥 Wildfire Alert sent successfully via email 📧")
                    except Exception as e:
                        alert_status.error("Failed to send email alert")
                else:
                    alert_status.error("Email alerts not configured")
            else:
                st.success("✅ Area appears to be safe from wildfires")
            
            # 3. User Feedback (No local saving)
            st.divider()
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("Is this result incorrect?")
            with col2:
                if st.button("Report False Positive"):
                    # Log report to console instead of saving image
                    print(f"[USER REPORT] {datetime.now()} - False Positive reported for current image")
                    st.toast("✅ Detection reported. Thank you for your feedback!")
                    st.info("Thank you! Your feedback has been logged for system improvement.")
                
        except Exception as e:
            st.error(
                "Sorry, we couldn't analyze your image. "
                "Please ensure you uploaded a clear satellite image in JPG or PNG format."
            )
            print(f"Prediction Error: {e}")