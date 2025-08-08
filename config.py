"""
Configuration file for SmokeSignal-AI
Set up your email credentials and other settings here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email Configuration
EMAIL_CONFIG = {
    "EMAIL_ADDRESS": os.getenv("EMAIL_ADDRESS", ""),
    "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD", ""),
    "TARGET_EMAIL": os.getenv("TARGET_EMAIL", "admin@example.com"),
}

# Model Configuration
MODEL_CONFIG = {
    "MODEL_PATH": "model/wildfire_detector_model.keras",
    "CONFIDENCE_THRESHOLD": 0.5,
}

# Application Configuration
APP_CONFIG = {
    "PAGE_TITLE": "SmokeSignal-AI",
    "PAGE_ICON": "🔥",
    "LAYOUT": "centered",
}

def check_email_configuration():
    """
    Check if email configuration is properly set up.
    """
    email_address = EMAIL_CONFIG["EMAIL_ADDRESS"]
    email_password = EMAIL_CONFIG["EMAIL_PASSWORD"]
    
    if not email_address or not email_password:
        return False, "Email credentials not configured"
    
    return True, "Email configuration is valid"

def get_configuration_status():
    """
    Get the status of all configurations.
    """
    status = {
        "email_configured": check_email_configuration()[0],
        "model_exists": os.path.exists(MODEL_CONFIG["MODEL_PATH"]),
        "email_address": EMAIL_CONFIG["EMAIL_ADDRESS"] if EMAIL_CONFIG["EMAIL_ADDRESS"] else "Not set",
        "target_email": EMAIL_CONFIG["TARGET_EMAIL"],
    }
    return status 