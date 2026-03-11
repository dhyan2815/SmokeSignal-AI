from datetime import datetime
from src.utils.alerts import send_email_alert

def trigger_fire_alert(prediction_result: dict):
    """
    Triggers a wildfire alert if the prediction result indicates a wildfire.
    Sends an email alert using the details from the prediction.
    """
    if prediction_result.get("label") == "Wildfire":
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        confidence = prediction_result.get("confidence", 0.0)
        
        # The send_email_alert function in src/utils/alerts.py
        # retrieves target_email from Config.TARGET_EMAIL.
        # It expects timestamp, confidence_score, and image_info.
        send_email_alert(
            timestamp=current_time,
            confidence_score=confidence,
            image_info={"source": "SmokeSignal AI Detection"} # Example image info
        )
        return {"status": "Alert sent"}
    return {"status": "No alert triggered"}
