from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import io
from PIL import Image
from src.services.inference_service import run_inference
from src.api.routes_inference import router as inference_router
from src.api.routes_alert import router as alerts_router

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

app.include_router(inference_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")

@app.get("/ui", response_class=HTMLResponse)
async def ui_home(request: Request):
    """Simple HTML form for testing inference."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ui/predict", response_class=HTMLResponse)
async def ui_predict(request: Request, file: UploadFile = File(...)):
    """Handle upload from HTML form."""
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        result = run_inference(image)
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "label": result.get("label", "Error"),
                "confidence": round(result.get("confidence", 0.0), 2)
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "label": "Error",
                "confidence": str(e)
            },
        )
