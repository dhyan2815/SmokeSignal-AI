# SmokeSignal AI

SmokeSignal AI is a Streamlit-based wildfire detection application that uses a trained CNN model to analyze aerial or satellite imagery and flag potential wildfire events with confidence scores.

## Table of Contents
- [SmokeSignal AI](#smokesignal-ai)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Key Features](#key-features)
  - [Architecture Diagrams](#architecture-diagrams)
    - [Activity Diagram](#activity-diagram)
    - [Sequence Diagram](#sequence-diagram)
    - [Data Flow Diagram (DFD)](#data-flow-diagram-dfd)
    - [Entity-Relationship (ER) Diagram](#entity-relationship-er-diagram)
  - [Tech Stack](#tech-stack)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Run the App](#run-the-app)
  - [How It Works](#how-it-works)
  - [Feedback Workflow](#feedback-workflow)
  - [Troubleshooting](#troubleshooting)
  - [Future Improvements](#future-improvements)
  - [Author](#author)

## Overview
The app accepts an uploaded image, validates whether it is likely in-domain (aerial/satellite style), preprocesses it for the model, runs wildfire inference, and optionally sends email alerts when a wildfire is detected.

## Key Features
- CNN-based wildfire detection with confidence scoring
- Out-of-distribution (OOD) scene validation before inference
- Streamlit UI for quick upload and analysis
- Automatic email alerting for positive detections
- User feedback reporting (false positive / false negative)

## Architecture Diagrams
The project architecture assets are in the [`architecture`](architecture) folder.

- [Activity Diagram](architecture/activity_diagram.png)
- [Sequence Diagram](architecture/sequence_diagram.png)
- [Data Flow Diagram (DFD)](architecture/dfd_diagram.png)
- [Entity-Relationship (ER) Diagram](architecture/er_diagram.png)

### Activity Diagram
![Activity Diagram](architecture/activity_diagram.png)

### Sequence Diagram
![Sequence Diagram](architecture/sequence_diagram.png)

### Data Flow Diagram (DFD)
![Data Flow Diagram](architecture/dfd_diagram.png)

### Entity-Relationship (ER) Diagram
![ER Diagram](architecture/er_diagram.png)

## Tech Stack
- Python
- Streamlit
- TensorFlow / Keras
- NumPy
- Pillow
- OpenCV (headless)
- python-dotenv

## Project Structure
```text
SmokeSignal-AI/
- app.py                      # Streamlit entry point
- config.py                   # Environment and app configuration
- requirements.txt            # Python dependencies
- architecture/               # System diagrams (ER, DFD, Sequence, Activity)
- assets/                     # Static assets used in README/UI
- model/                      # Trained model (.keras)
- utils/
  - alerts.py                 # Alert and feedback email logic
  - ood.py                    # OOD detector using MobileNetV2
  - preprocess.py             # Image preprocessing utilities
- src/                        # Additional source modules
- data/                       # Data assets
- notebooks/                  # Experiments and research notebooks
```

## Prerequisites
- Python 3.10+ recommended
- Internet access for first-time MobileNetV2 weights download (OOD detector)

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Create or update `.env` in the project root:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
TARGET_EMAIL=recipient@example.com
```

Notes:
- Email alerts are enabled only when `EMAIL_ADDRESS` and `EMAIL_PASSWORD` are set.
- `TARGET_EMAIL` defaults to `admin@example.com` if not provided.

## Run the App
```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit (usually `http://localhost:8501`).

## How It Works
1. User uploads a JPG/PNG image.
2. OOD detector screens for non-aerial/non-satellite scenes.
3. Image is resized and normalized to model input requirements.
4. CNN predicts wildfire probability.
5. If score is above threshold, app labels wildfire and sends alert email (if configured).

## Feedback Workflow
After each prediction, the app allows reporting:
- False Positive (if model says wildfire but user disagrees)
- False Negative (if model says no wildfire but user disagrees)

When email is configured, feedback is also sent via email for model monitoring.

## Troubleshooting
- `Model file not found`: Ensure `model/wildfire_detector_model.keras` exists.
- `Email authentication failed`: Use an app password (not account password) for Gmail SMTP.
- `OOD model download issues`: Ensure network access on first run.
- Unsupported image errors: Use clear JPG/PNG aerial or satellite imagery.

## Future Improvements
- Add automated test suite (`pytest`)
- Add metrics dashboard for feedback trends
- Add geolocation metadata support for alerts
- Add containerized deployment configuration

## Author
Dhyan Patel
- GitHub: [@dhyan2815](https://github.com/dhyan2815)
- LinkedIn: [Dhyan Patel](https://linkedin.com/in/dhyan-patel)
- Portfolio: [Dhyan Patel]([https://](https://dhyan-patel.framer.website/))
