from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io
from src.services.inference_service import predict_fire

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # ✅ await the read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")  # ✅ Convert to normal RGB image
        result = await predict_fire(image)  # depends on how your inference service works
        return {"prediction": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    