import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_PATH = os.getenv("MODEL_PATH")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
