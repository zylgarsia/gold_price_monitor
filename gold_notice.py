import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = int(os.environ["SMTP_PORT"])
EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECEIVER = os.environ["EMAIL_RECEIVER"]


def send_email(subject, content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = Header(subject, "utf-8")

    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()
