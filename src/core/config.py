from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "SmokeSignalAI"
    environment: str = "development"
    log_level: str = "INFO"
    model_path: str = "model/wildfire_detector_model.keras"
    confidence_threshold: float = 0.8
    email_address: str = ""
    email_password: str = ""
    target_email: str = ""
    SECRET_KEY: str = "default-secret-key-change-in-production"
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASS: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
