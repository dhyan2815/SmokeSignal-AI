from fastapi import FastAPI
from src.api.routes_inference import router as inference_router
from src.api.routes_alert import router as alerts_router
from src.core.exceptions import ExceptionMiddleware

from src.core.config import settings
print(settings.model_path)

from src.core.logger import logger
logger.info("Model loaded successfully.")

app = FastAPI(title="SmokeSignal AI")

# Routers
app.include_router(inference_router, prefix="/api", tags=["Inference"])
app.include_router(alerts_router, prefix="/api", tags=["Alerts"])

# Global exception middleware
app.add_middleware(ExceptionMiddleware)

@app.get("/")
def root():
    return {"message": "SmokeSignal AI Backend is running 🚀"}
