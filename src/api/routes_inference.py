from fastapi import APIRouter, UploadFile, File, Depends
from src.services.inference_service import run_inference
from src.core.dependencies import get_model
from src.core.config import settings
import io
from PIL import Image

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...), model=Depends(get_model)):
    contents = await file.read() # Read the file contents
    image = Image.open(io.BytesIO(contents)).convert("RGB") # Create a PIL Image
    result = run_inference(image)
    return result
