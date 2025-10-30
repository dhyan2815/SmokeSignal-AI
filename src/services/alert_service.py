from src.utils.notifier import send_alert

def handle_alert(prediction: dict, threshold: float = 0.8):
    """Trigger alert if confidence exceeds threshold."""
    if prediction.get("label") == "Wildfire" and prediction.get("confidence", 0) >= threshold:
        send_alert(prediction)
        return {"alert_triggered": True, "message": "Emergency alert sent."}
    return {"alert_triggered": False, "message": "No alert necessary."}
