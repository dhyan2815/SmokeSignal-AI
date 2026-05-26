"""
Configuration file for SmokeSignal-AI
Set up your email credentials and other settings here.
"""

import os
from dotenv import load_dotenv

# Load .env file if it exists (for development)
load_dotenv()

class Config:
    """Configuration class for SmokeSignal-AI"""
    
    # Email Configuration
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    TARGET_EMAIL = os.environ.get("TARGET_EMAIL", "admin@example.com")
    
    # Model Configuration
    MODEL_PATH = "model/wildfire_detector_model.keras"
    
    # Detection Configuration
    CONFIDENCE_THRESHOLD = 0.5
    
    @classmethod
    def is_email_configured(cls):
        """Check if email configuration is complete"""
        return bool(cls.EMAIL_ADDRESS and cls.EMAIL_PASSWORD)
    
    @classmethod
    def get_email_config_status(cls):
        """Get detailed email configuration status"""
        status = {
            "email_address": bool(cls.EMAIL_ADDRESS),
            "email_password": bool(cls.EMAIL_PASSWORD),
            "target_email": cls.TARGET_EMAIL,
            "fully_configured": cls.is_email_configured()
        }
        return status
    
    @classmethod
    def debug_environment(cls):
        """Debug environment variables for troubleshooting"""
        debug_info = {
            "environment_variables": {
                "EMAIL_ADDRESS": "SET" if cls.EMAIL_ADDRESS else "NOT SET",
                "EMAIL_PASSWORD": "SET" if cls.EMAIL_PASSWORD else "NOT SET",
                "TARGET_EMAIL": cls.TARGET_EMAIL
            },
            "email_configured": cls.is_email_configured(),
            "env_file_loaded": os.path.exists(".env")
        }
        return debug_info 