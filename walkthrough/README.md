# SmokeSignal AI - Walkthrough Guide

## Overview

SmokeSignal AI is a CNN-based wildfire detection system that analyzes satellite imagery to identify potential wildfires and sends automated email alerts to emergency contacts. The system uses a TensorFlow/Keras deep learning model for image classification.

## Project Structure

```
SmokeSignal-AI/
├── src/                          # Main Python source code
│   ├── main.py                   # FastAPI application entry point
│   ├── cli.py                    # Command-line interface for inference
│   ├── api/                      # API route handlers
│   │   ├── routes_inference.py   # Prediction endpoint (/api/predict)
│   │   └── routes_alert.py       # Alert trigger endpoint (/api/trigger-alert)
│   ├── core/                     # Core application components
│   │   ├── config.py             # Configuration settings (from .env)
│   │   ├── dependencies.py       # Dependency injection (model loading)
│   │   ├── exceptions.py         # Custom exception handling middleware
│   │   └── logger.py             # Logging setup
│   ├── services/                 # Business logic services
│   │   ├── inference_service.py # Model inference and preprocessing
│   │   ├── alert_service.py     # Alert triggering logic
│   │   └── auth_service.py      # Authentication service
│   └── utils/                    # Utility functions
│       ├── alerts.py             # Email sending utilities
│       ├── preprocess.py         # Image preprocessing
│       ├── notifier.py           # Notification utilities
│       └── tui.py                # Terminal UI components
├── model/                        # Trained model
│   └── wildfire_detector_model.keras  # Keras model file
├── frontend/                      # React + Vite frontend
├── notebooks/                     # Jupyter notebooks for model training
├── requirements.txt              # Python dependencies
└── .env                          # Environment configuration
```

## What SmokeSignal AI Includes

### 1. Backend (FastAPI)
- **REST API** for image prediction and alert triggering
- **CORS middleware** for frontend communication
- **Exception handling** via custom middleware

### 2. Deep Learning Model
- **TensorFlow/Keras CNN** trained on wildfire satellite imagery
- Input: Satellite images (auto-resized to 64x64)
- Output: Binary classification (Wildfire / No Fire) with confidence score

### 3. Alert System
- **SMTP email integration** (Gmail)
- Automated alerts when wildfire is detected
- Configurable via environment variables

### 4. CLI Tool
- Terminal-based image inference with progress indicators
- Rich console output for results

### 5. Frontend (React + Vite)
- Modern React 19 frontend with Tailwind CSS
- Image upload and visualization
- Charts and analytics

## How to Operate

### Prerequisites

1. **Python 3.8+** installed
2. **Node.js 18+** (for frontend)
3. **Gmail account** with App Password (for email alerts)

### Installation

```bash
# Clone the repository
git clone https://github.com/dhyan2815/SmokeSignal-AI.git
cd SmokeSignal-AI

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
```

### Configuration

Create or update the `.env` file in the root directory:

```env
# Model Settings
MODEL_PATH=model/wildfire_detector_model.keras
CONFIDENCE_THRESHOLD=0.8

# SMTP Email Settings (for alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
TARGET_EMAIL=emergency_recipient@example.com
```

> **Note**: To send emails via Gmail, you need to enable 2-Factor Authentication and generate an App Password. Do not use your regular password.

### Running the Backend (FastAPI)

```bash
# From project root
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. API documentation at `http://localhost:8000/docs`.

### Running the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173` (default Vite port).

### Using the CLI

```bash
python src/cli.py <path_to_image>
```

Example:
```bash
python src/cli.py test_images/satellite_photo.jpg
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/predict` | POST | Upload image for wildfire detection |
| `/api/trigger-alert` | POST | Manually trigger an alert |

### Testing the API

```bash
# Using curl
curl -X POST -F "file=@test.jpg" http://localhost:8000/api/predict
```

---

## Announcements, Issues & Suggestions

### Known Issues

1. **Model Loading on Startup**: The TensorFlow model loads at application startup via `get_model()`. If the model file is missing or corrupted, the application will fail to start. Ensure `wildfire_detector_model.keras` exists in the `model/` directory.

2. **CORS Configuration**: Currently set to allow all origins (`["*"]`). For production, restrict to your frontend URL.

3. **Email Alert Limitations**: 
   - Only Gmail SMTP is configured by default
   - No retry mechanism for failed email sends
   - Alerts are sent immediately without batching

4. **Image Size Handling**: Images are resized to 64x64 which may lose detail for complex satellite imagery.

### Suggestions for Improvement

1. **Model Improvements**:
   - Upgrade to a larger input size (e.g., 224x224) for better accuracy
   - Consider using transfer learning with ResNet or EfficientNet
   - Add model versioning and A/B testing support

2. **Alert System Enhancements**:
   - Add support for multiple notification channels (Slack, SMS, Webhooks)
   - Implement alert batching to reduce spam
   - Add retry logic with exponential backoff

3. **API Improvements**:
   - Add rate limiting to prevent abuse
   - Implement authentication (JWT/API keys)
   - Add request validation for image file types/sizes

4. **Frontend Enhancements**:
   - Add image history/predictions dashboard
   - Implement real-time notifications
   - Add batch processing support

5. **Deployment**:
   - Add Docker support for containerized deployment
   - Add Kubernetes manifests for scaling
   - Set up CI/CD pipeline

### Upcoming Features (Roadmap)

- [ ] Docker containerization
- [ ] Multi-channel alerts (SMS, Slack, Discord)
- [ ] Model version management
- [ ] Batch image processing
- [ ] User authentication system
- [ ] Prediction history database

---

## Support

For bugs or feature requests, open an issue at: https://github.com/dhyan2815/SmokeSignal-AI/issues