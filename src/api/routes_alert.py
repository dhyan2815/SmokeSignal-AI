from fastapi import APIRouter
from src.services.alert_service import trigger_fire_alert

router = APIRouter()

@router.post("/trigger-alert")
async def trigger_alert(prediction: dict):
    """Test manual alert triggering (for debugging)."""
    return trigger_fire_alert(prediction)
