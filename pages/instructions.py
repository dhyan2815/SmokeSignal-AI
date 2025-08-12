import streamlit as st


st.title("📋 How to Use SmokeSignal-AI")
st.markdown("---")

# Quick Start Section
st.header("🚀 Quick Start Guide")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload an Image")
    st.markdown("""
    - Use the file uploader on the main page
    - Supported formats: **JPG, JPEG, PNG**
    - Any satellite or aerial image will work
    """)

with col2:
    st.subheader("2. Enable Email Alerts (Optional)")
    st.markdown("""
    - Check "Enable Email Alerts" in the sidebar
    - Configure your `.env` file with Gmail credentials
    - Receive instant notifications for detected wildfires
    """)

st.markdown("---")

# Detailed Instructions
st.header("📖 Detailed Instructions")

st.subheader("### Step-by-Step Process")

st.markdown("""
1. **Navigate to the Main Page**: Go to the "🔥 Wildfire Detection" page
2. **Upload Your Image**: Click "Browse files" and select a satellite image
3. **Wait for Analysis**: The AI will process the image automatically
4. **Review Results**: You'll see either:
   - 🔥 **Wildfire Detected** - with confidence score and timestamp
   - ✅ **No Wildfire Detected** - indicating the area is safe
5. **Email Alerts**: If enabled, you'll receive detailed notifications
""")

st.markdown("---")

# What the AI Detects
st.header("🔍 What the AI Detects")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🔥 Active Fire Indicators:**
    - Smoke plumes
    - Bright thermal signatures
    - Active fire areas
    - Flame patterns
    """)

with col2:
    st.markdown("""
    **🌿 Environmental Changes:**
    - Burn scars
    - Thermal anomalies
    - Vegetation changes
    - Heat patterns
    """)

st.markdown("---")

# Demo Examples
st.header("📊 Demo Examples")

# Example 1
with st.expander("🔥 Example 1: Wildfire Detection", expanded=True):
    st.markdown("""
    **Scenario**: Uploading a satellite image with visible smoke plumes
    
    **Result**:
    - 🔥 **Wildfire Detected**
    - Confidence: 87.5%
    - Timestamp: 2024-01-15 14:30:25
    - Email Alert: ✅ Sent successfully
    """)

# Example 2
with st.expander("✅ Example 2: Safe Area", expanded=True):
    st.markdown("""
    **Scenario**: Uploading a clear forest area image
    
    **Result**:
    - ✅ **No Wildfire Detected**
    - Confidence: 12.3%
    - Status: Area appears safe from wildfires
    """)

# Example 3
with st.expander("🚨 Example 3: High Confidence Detection", expanded=True):
    st.markdown("""
    **Scenario**: Uploading an active fire zone image
    
    **Result**:
    - 🔥 **Wildfire Detected**
    - Confidence: 94.2%
    - Alert: 🚨 High-priority detection
    - Email: Detailed alert with confidence score sent
    """)

st.markdown("---")

# Email Configuration
st.header("📧 Email Alert Setup")

st.markdown("""
### Setting Up Email Alerts

1. **Create a `.env` file** in the project root with:
   ```env
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   TARGET_EMAIL=admin@example.com
   ```

2. **Get Gmail App Password**:
   - Go to Google Account settings
   - Enable 2-Step Verification
   - Go to Security > App passwords
   - Generate password for "Mail"

3. **Enable in App**:
   - Check "Enable Email Alerts" in sidebar
   - Verify configuration status shows ✅
""")

st.markdown("---")

# Troubleshooting
st.header("🔧 Troubleshooting")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Common Issues:**
    
    **Email Not Sending:**
    - Check Gmail app password
    - Verify 2-Step Verification is enabled
    - Confirm email addresses are correct
    
    **Model Loading Error:**
    - Ensure model file exists
    - Check TensorFlow installation
    """)

with col2:
    st.markdown("""
    **Image Processing:**
    
    **Upload Errors:**
    - Verify image format (JPG, PNG)
    - Check file integrity
    - Ensure file size is reasonable
    
    **Analysis Failures:**
    - Try different image
    - Check image quality
    - Verify image has content
    """)

st.markdown("---")

# Technical Details
st.header("⚙️ Technical Details")

st.markdown("""
### Model Architecture
- **Framework**: TensorFlow/Keras
- **Input**: Satellite images (automatically resized)
- **Output**: Binary classification with confidence scores
- **Processing**: Real-time analysis with preprocessing pipeline

### Preprocessing Pipeline
1. **Image Loading**: Multi-format support
2. **Resizing**: Automatic dimension adjustment
3. **Normalization**: Pixel value scaling [0, 1]
4. **Batch Processing**: Model-ready format

### Alert System
- **SMTP Integration**: Gmail SMTP for reliability
- **Rich Content**: Timestamps, confidence scores, details
- **Error Handling**: Graceful failure with user feedback
""")

st.markdown("---")

# Support
st.header("💬 Need Help?")

st.markdown("""
If you encounter any issues:

1. **Check the console output** for error messages
2. **Verify all dependencies** are installed
3. **Ensure proper file permissions**
4. **Review the troubleshooting section** above

For additional support, please refer to the project documentation or create an issue in the repository.
""")

st.markdown("---")

st.markdown("**SmokeSignal-AI** - Protecting our planet, one image at a time. 🌍🔥") 