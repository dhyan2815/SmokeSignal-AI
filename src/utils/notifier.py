def send_alert(prediction: dict):
    """Simulate sending an alert. Replace with actual email/SMS integration later."""
    print(f"🚨 ALERT: {prediction['label']} detected with confidence {prediction['confidence']:.2f}")
