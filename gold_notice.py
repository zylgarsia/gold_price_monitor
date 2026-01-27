import sys
sys.stdout.reconfigure(encoding='utf-8')
# notifier.py
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import *

def send_email(subject, content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = Header(subject, "utf-8")

    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()
