"""SMTP Mail handler"""

import smtplib
from email.mime.multipart import MIMEMultipart

from confs import *

def send_mail(msg, dest):
    """Forward the email based on the FROM address"""
    forward_msg = MIMEMultipart()
    forward_msg["From"] = EMAIL_FROM
    forward_msg["To"] = dest
    forward_msg["Subject"] = msg["subject"]

    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        forward_msg.attach(part)

    # Send the forwarded email
    try:
        if SECURITY == "ssl":
            smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        elif SECURITY == "starttls":
            smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp.starttls()
        else:
            raise ValueError("Invalid security configuration: should be either 'ssl' or 'starttls'")

        smtp.login(USERNAME, PASSWORD)
        smtp.sendmail(USERNAME, dest, forward_msg.as_string())
        smtp.quit()
    except Exception as e:
        print("Error forwarding email:", str(e))
