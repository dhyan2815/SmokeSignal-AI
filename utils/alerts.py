import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

def send_email_alert(timestamp, confidence_score=None, image_info=None):
    """
    Send email alert when wildfire is detected.
    
    Args:
        timestamp (str): Detection timestamp
        confidence_score (float, optional): Model confidence score
        image_info (str, optional): Additional image information
    """
    try:
        # Get email configuration from environment variables
        email_address = os.environ.get("EMAIL_ADDRESS")
        email_password = os.environ.get("EMAIL_PASSWORD")
        target_email = os.environ.get("TARGET_EMAIL", "admin@example.com")
        
        # Check if email credentials are configured
        if not email_address or not email_password:
            raise ValueError("Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
        
        # Create email message
        msg = EmailMessage()
        
        # Build email content
        subject = "Wildfire Detected! - SmokeSignal-AI"
        content = f"""
🔥 WILDFIRE DETECTION ALERT 🔥

Detection Time: {timestamp}
Model: SmokeSignal-AI Wildfire Detector

⚠️ A potential wildfire has been detected in the analyzed satellite image.

"""
        
        if confidence_score is not None:
            content += f"Confidence Score: {confidence_score:.2%}\n\n"
        
        if image_info:
            content += f"Image Information: {image_info}\n\n"
        
        content += """
IMMEDIATE ACTION REQUIRED:
1. Verify the detection with additional sources
2. Contact local emergency services if confirmed
3. Monitor the area for further developments

This is an automated alert from SmokeSignal-AI.
Please verify all detections before taking action.

---
SmokeSignal-AI - AI-Powered Wildfire Detection System
"""
        
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = target_email

        # Send email via Gmail SMTP
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_address, email_password)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        raise Exception("Email authentication failed. Please check your email credentials.")
    except smtplib.SMTPException as e:
        raise Exception(f"SMTP error occurred: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to send email alert: {str(e)}")

def test_email_configuration():
    """
    Test email configuration without sending an actual alert.
    """
    try:
        email_address = os.environ.get("EMAIL_ADDRESS")
        email_password = os.environ.get("EMAIL_PASSWORD")
        
        if not email_address or not email_password:
            return False, "Email credentials not configured"
        
        # Test connection
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_address, email_password)
        server.quit()
        
        return True, "Email configuration is valid"
        
    except Exception as e:
        return False, f"Email configuration test failed: {str(e)}"

