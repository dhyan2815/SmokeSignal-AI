from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "SmokeSignalAI"
    environment: str = "development"
    log_level: str = "INFO"
    model_path: str = "artifacts/model/wildfire_detector.pt"
    confidence_threshold: float = 0.8

    class Config:
        env_file = ".env"

settings = Settings()
