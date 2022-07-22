import httplib2
from util.colors import ESC, YELLOW
from util.parse_json import parse_json
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from util.print_log import error, info
import base64
from googleapiclient import errors, discovery
import oauth2client
from oauth2client import client, tools, file


CLIENT_SECRET_FILE = "data/client_secret.json"
APPLICATION_NAME = 'Gmail API Python Send Email'
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
port = 465
all_receivers = parse_json("data/config.json")["kindle_email"]
all_notification = parse_json("data/config.json")["notification_email"]


def get_credentials():
    credential_dir = ".credentials"
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "gmail-email-send.json")
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print(f"Storing credentials to {credential_path}")
    return credentials


def send_mail(fp: str):
    send(message_main(fp))
    print(f"\t{YELLOW}DONE{ESC}")
    return True


def send_notification(title: str, msg: str):
    send(message_notification(title, msg))
    print(f"\t{YELLOW}DONE{ESC}")
    return True


def send(message):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("gmail", "v1", http=http)
    try:
        (service.users().messages().send(userId="me", body=message).execute())
    except errors.HttpError as error:
        print(f"An error occured {error}")


def message_main(fp: str):
    filename = os.path.basename(fp)
    message = MIMEMultipart()
    message["Subject"] = "convert"
    message["To"] = ", ".join(all_receivers)

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

    info(f"Sending {YELLOW}{filename}{ESC} by mail", end="")
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


def message_notification(title: str, msg: str):
    message = MIMEText(msg)
    message["Subject"] = f"AutoMangaDownloader - {title}"
    message["To"] = ", ".join(all_notification)

    info(f"Sending notification: '{YELLOW}{title}{ESC}'", end="")
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}
