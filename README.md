# SmokeSignal AI

**An Deep Learning model based wildfire detection system** that analyzes satellite images to identify potential wildfires and sends automated alerts to emergency services.

## Features

- **AI-Powered Detection**: Deep learning model for accurate wildfire identification
- **Real-time Analysis**: Instant processing with confidence scoring
- **Automated Alerts**: Email notifications to fire stations and emergency services
- **User-Friendly Interface**: Clean, professional Streamlit web application
- **Multi-Page Navigation**: Organized help and instructions
- **Secure Configuration**: Environment-based email setup
- **Confidence Scoring**: Detailed detection confidence levels

## How SmokeSignal AI works?

### Simple 3-Step Process

1. **Upload Image**
   - Click "Browse files" on the main page
   - Select any satellite/aerial image (JPG, PNG)
   - Image is automatically processed

2. **AI Analysis**
   - System analyzes for wildfire indicators
   - Detects smoke plumes, fire areas, thermal signatures
   - Provides confidence score (0-100%)

3. **Results & Alerts**
   - **Wildfire Detected**: Shows confidence, timestamp, email alert
   - **No Wildfire**: Confirms area is safe
   - **Email Alerts**: Instant notifications to emergency services

### Email Alert Configuration

1. **Enable Alerts**: Check "Enable Email Alerts" in sidebar
2. **Verify Status**: Confirm email credentials are loaded
3. **Receive Notifications**: Get instant alerts for detected wildfires

##  Demo Examples

### Example 1: Wildfire Detection
```
Upload: satellite_image_with_smoke.jpg
Result: 🔥 Wildfire Detected
Confidence: 87.5%
Alert: Email sent to fire station
Timestamp: 2024-01-15 14:30:25
```

### Example 2: Safe Area
```
Upload: clear_forest_area.jpg
Result: ✅ No Wildfire Detected
Confidence: 12.3%
Status: Area appears safe
```

### Example 3: High Confidence Detection
```
Upload: active_fire_zone.jpg
Result: 🔥 Wildfire Detected
Confidence: 94.2%
Alert: High-priority notification sent
```

## What the SmokeSignal Detects

###  Active Fire Indicators
- Smoke plumes and visible fire
- Bright thermal signatures
- Active fire areas and flame patterns

###  Environmental Changes
- Burn scars and damage areas
- Thermal anomalies and heat patterns
- Vegetation changes indicating fire activity

##  Technical Architecture

### Model Framework
- **Framework**: TensorFlow/Keras
- **Input**: Satellite images (auto-resized)
- **Output**: Binary classification with confidence scores
- **Processing**: Real-time analysis pipeline

### Preprocessing Pipeline
1. **Image Loading**: Multi-format support (JPG, PNG)
2. **Resizing**: Automatic dimension adjustment
3. **Normalization**: Pixel values scaled to [0, 1]
4. **Batch Processing**: Model-ready format

### Alert System
- **SMTP Integration**: Gmail SMTP for reliability
- **Rich Content**: Timestamps, confidence scores, details
- **Error Handling**: Graceful failure with user feedback

## User Interface Features

- **Clean detection interface** with file uploader
- **Expandable instructions** for quick help
- **Real-time analysis** with progress indicators
- **Professional results display** with confidence scores

## Acknowledgments

- **TensorFlow/Keras** for deep learning framework
- **Streamlit** for the web application framework
- **OpenCV** for image processing capabilities
- **Gmail SMTP** for reliable email delivery

---

**SmokeSignal-AI** - Protecting our planet, one image at a time. 🌍🔥

*Empowering emergency services with AI-driven wildfire detection technology.* 