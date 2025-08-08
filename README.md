# 🔥 SmokeSignal-AI

An AI-powered wildfire detection system that analyzes satellite images to identify potential wildfires and sends automated alerts.

## Features

- **AI-Powered Detection**: Uses deep learning to detect wildfires in satellite imagery
- **Real-time Analysis**: Instant processing of uploaded images
- **Email Alerts**: Automated notifications when wildfires are detected
- **User-friendly Interface**: Clean Streamlit web interface
- **Confidence Scoring**: Provides confidence levels for detections

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Email Alerts (Optional)

Create a `.env` file in the project root:

```env
# Email Configuration
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
TARGET_EMAIL=admin@example.com
```

**Note**: For Gmail, you need to use an App Password:
1. Enable 2-Step Verification in your Google Account
2. Go to Security > App passwords
3. Generate a new app password for "Mail"
4. Use that password in EMAIL_PASSWORD

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## How to Use

### Basic Usage

1. **Upload an Image**: Use the file uploader to select a satellite image (JPG, JPEG, PNG)
2. **Automatic Analysis**: The AI will analyze the image for wildfire indicators
3. **View Results**: You'll see either:
   - 🔥 **Wildfire Detected** - with confidence score and timestamp
   - ✅ **No Wildfire Detected** - indicating the area is safe

### Email Alerts

1. **Enable Alerts**: Check the "Enable Email Alerts" option in the sidebar
2. **Configure Email**: Set up your email credentials in the `.env` file
3. **Receive Notifications**: Get instant alerts when wildfires are detected

## Demo Examples

### Example 1: Wildfire Detection
```
Upload: satellite_image_with_smoke.jpg
Result: 🔥 Wildfire Detected
Confidence: 87.5%
Alert: Email notification sent
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
Alert: High-priority email sent
```

## What the AI Detects

- **Smoke Plumes**: Visible smoke from active fires
- **Active Fire Areas**: Bright thermal signatures
- **Burn Scars**: Areas recently affected by fires
- **Thermal Anomalies**: Unusual heat patterns

## Technical Details

### Model Architecture
- **Framework**: TensorFlow/Keras
- **Input**: Satellite images (resized to model specifications)
- **Output**: Binary classification (wildfire/no wildfire) with confidence scores

### Preprocessing Pipeline
1. **Image Loading**: Supports multiple formats (JPG, PNG)
2. **Resizing**: Automatic resizing to model input dimensions
3. **Normalization**: Pixel values scaled to [0, 1] range
4. **Batch Processing**: Ready for model inference

### Alert System
- **SMTP Integration**: Gmail SMTP for reliable delivery
- **Rich Content**: Detailed alerts with timestamps and confidence scores
- **Error Handling**: Graceful failure with user feedback

## File Structure

```
SmokeSignal-AI/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── model/
│   └── wildfire_detector_model.keras  # Trained model
├── utils/
│   ├── alerts.py         # Email alert system
│   └── preprocess.py     # Image preprocessing utilities
└── notebooks/
    └── SmokeSignal-AI.ipynb  # Development notebook
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_ADDRESS` | Gmail address for sending alerts | Required |
| `EMAIL_PASSWORD` | Gmail app password | Required |
| `TARGET_EMAIL` | Email address for receiving alerts | admin@example.com |

### Model Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `CONFIDENCE_THRESHOLD` | 0.5 | Minimum confidence for wildfire detection |
| `MODEL_PATH` | model/wildfire_detector_model.keras | Path to trained model |

## Troubleshooting

### Common Issues

1. **Email Not Sending**
   - Check your Gmail app password
   - Ensure 2-Step Verification is enabled
   - Verify email addresses are correct

2. **Model Loading Error**
   - Ensure the model file exists in `model/` directory
   - Check TensorFlow installation

3. **Image Processing Error**
   - Verify image format (JPG, JPEG, PNG)
   - Check image file integrity

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure proper file permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**SmokeSignal-AI** - Protecting our planet, one image at a time. 🌍🔥 