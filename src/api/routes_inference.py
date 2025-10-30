from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # ✅ await the read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")  # ✅ Convert to normal RGB image
        result = await run_inference(image)  # depends on how your inference service works
        return {"prediction": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    