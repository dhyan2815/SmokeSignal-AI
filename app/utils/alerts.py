import smtplib
from email.message import EmailMessage

def send_email_alert(timestamp):
    msg = EmailMessage()
    msg.set_content(f"🔥 Wildfire detected at {timestamp}")
    msg['Subject'] = 'SmokeSignal-AI ALERT'
    msg['From'] = "your_email@gmail.com"
    msg['To'] = "target_email@example.com"

    # Replace with environment variables in production
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("your_email@gmail.com", "your_password")
    server.send_message(msg)
    server.quit()
