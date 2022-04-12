import smtplib
import ssl
from util.colors import ESC, YELLOW
from util.parse_json import parse_json
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

from util.print_log import error, info


username, password = parse_json("data/login.json").values()
port = 465
all_receivers = parse_json("data/config.json")["kindle_email"]
all_notification = parse_json("data/config.json")["notification_email"]


def send_mail(fp: str):
    filename = os.path.basename(fp)
    message = MIMEMultipart()
    message["From"] = username
    message["Subject"] = "convert"
    
    with open(fp, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    filename = os.path.basename(fp)

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename = {filename}"
    )
    message.attach(part)
    text = message.as_string()
    
    info(f"Sending {YELLOW}{filename}{ESC} by mail", end="")
    message["To"] = ", ".join(all_receivers)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, all_receivers, text)
    except smtplib.SMTPAuthenticationError:
        print()
        error(
            f"Invalid username and password given in {YELLOW}data/login.json{ESC}")
        exit(1)

    print(f"\t{YELLOW}DONE{ESC}")
    return True

def send_notification(title: str, msg: str):
    message = MIMEText(msg)
    message["From"] = username
    message["Subject"] = f"AutoMangaDownloader - {title}"
    text = message.as_string()
    
    info(f"Sending notification: '{YELLOW}{title}{ESC}'", end="")
    message["To"] = ", ".join(all_notification)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, all_notification, text)
    except smtplib.SMTPAuthenticationError:
        print()
        error(
            f"Invalid username and password given in {YELLOW}data/login.json{ESC}")
        exit(1)

    print(f"\t{YELLOW}DONE{ESC}")
    return True
