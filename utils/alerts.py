import smtplib
from email.message import EmailMessage
import os
import sys
from datetime import datetime

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def send_email_alert(timestamp, confidence_score=None, image_info=None):
    """
    Send email alert when wildfire is detected.
    
    Args:
        timestamp (str): Detection timestamp
        confidence_score (float, optional): Model confidence score
        image_info (str or dict, optional): Additional image information
    """
    try:
        # Get email configuration from Config class
        email_address = Config.EMAIL_ADDRESS
        email_password = Config.EMAIL_PASSWORD
        target_email = Config.TARGET_EMAIL
        
        # Check if email credentials are configured
        if not email_address or not email_password:
            raise ValueError("Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
        
        # Create email message
        msg = EmailMessage()

        # Subject
        subject = "🔥 Wildfire Detected — SmokeSignal‑AI"
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = target_email

        # Build plain text content
        lines = [
            "WILDFIRE DETECTION ALERT",
            "",
            f"Detection Time: {timestamp}",
            "System: SmokeSignal‑AI Wildfire Detector",
            "",
            "A potential wildfire has been DETECTED in the analyzed image.",
            "",
        ]
        if confidence_score is not None:
            lines.append(f"Confidence: {confidence_score:.2%}")
        if image_info:
            if isinstance(image_info, dict):
                lines.append("Image Info:")
                for k, v in image_info.items():
                    lines.append(f"- {k}: {v}")
            else:
                lines.append(f"Image Info: {image_info}")
            lines.append("")
        lines.extend([
            "IMMEDIATE ACTION REQUIRED:",
            "1) Verify the detection with additional sources",
            "2) Contact local emergency services if confirmed",
            "3) Monitor the area for further developments",
            "",
            "This is an automated alert from SmokeSignal‑AI. Please verify all detections before taking action.",
        ])
        content_text = "\n".join(lines)

        # Build HTML content
        confidence_html = f"<p><strong>Detection Level:</strong> {confidence_score:.2%}</p>" if confidence_score is not None else ""
        if image_info:
            if isinstance(image_info, dict):
                info_items = "".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in image_info.items()])
                image_info_html = f"<ul style=\"margin:0 0 12px 20px;\">{info_items}</ul>"
            else:
                image_info_html = f"<p><strong>Image Info:</strong> {image_info}</p>"
        else:
            image_info_html = ""

        content_html = f"""
<html>
  <body style="font-family:Segoe UI, Arial, sans-serif; color:#111;">
    <h2 style="margin:0 0 12px;">🔥 Wildfire Detection Alert</h2>
    <p style="margin:0 0 12px;"><strong>Detection Time:</strong> {timestamp}<br/>
       <strong>System:</strong> SmokeSignal‑AI Wildfire Detector</p>
    <p style="margin:0 0 12px;">⚠️ A potential wildfire has been <strong>detected</strong> in the analyzed image.</p>
    {confidence_html}
    {image_info_html}
    <h3 style="margin:16px 0 8px;">Immediate Action Required</h3>
    <ol style="margin:0 0 16px 20px;">
      <li>Verify the detection with additional sources</li>
      <li>Contact local emergency services if confirmed</li>
      <li>Monitor the area for further developments</li>
    </ol>
    <hr style="border:none;border-top:1px solid #eee;margin:16px 0;"/>
    <p style="font-size:12px;color:#555;margin:0;">This is an automated alert from SmokeSignal‑AI. Please verify all detections before taking action.</p>
  </body>
  </html>
"""

        # Attach both plain-text and HTML versions
        msg.set_content(content_text)
        msg.add_alternative(content_html, subtype='html')

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
        email_address = Config.EMAIL_ADDRESS
        email_password = Config.EMAIL_PASSWORD
        
        if not email_address or not email_password:
            return False, "Email credentials not configured"
        
        # Test connection
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_address, email_password)
        server.quit()
        
        return True, "Email configuration is valid"
        
    except Exception as e:
        return False, f"Email configuration test failed: {str(e)}"

