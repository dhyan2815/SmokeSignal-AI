from fastapi import APIRouter, UploadFile, File, Depends
from src.services.inference_service import run_inference
from src.services.alert_service import trigger_fire_alert
from src.core.dependencies import get_model
import io
from PIL import Image

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...), model=Depends(get_model)):
    contents = await file.read() # Read the file contents
    image = Image.open(io.BytesIO(contents)).convert("RGB") # Create a PIL Image
    result = run_inference(image)
    
    # Trigger alert if wildfire is detected
    if result.get("label") == "Wildfire":
        trigger_fire_alert(result)
        
    return result
