from fastapi import FastAPI
from src.api import routes_inference

app = FastAPI(title="SmokeSignal AI", version="2.0")

app.include_router(routes_inference.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "SmokeSignal AI API is running"}
