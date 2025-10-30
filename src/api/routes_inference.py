from fastapi import APIRouter, UploadFile, File, Depends
from src.services.inference_service import run_inference
from src.utils.preprocess import preprocess_image
from src.core.dependencies import get_model
from src.core.config import settings

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...), model=Depends(get_model)):
    image = preprocess_image(await file.read())
    result = run_inference(image)
    # optional: use threshold from settings
    threshold = settings.confidence_threshold
    result["alert"] = result["confidence"] >= threshold
    return result
