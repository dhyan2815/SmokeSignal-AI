from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes_inference import router as inference_router
from src.api.routes_alert import router as alerts_router
from src.core.exceptions import ExceptionMiddleware

app = FastAPI(title="SmokeSignal AI API")

# Register Exception Middleware
app.add_middleware(ExceptionMiddleware)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(inference_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "SmokeSignal AI API is running", "version": "1.0.0"}
