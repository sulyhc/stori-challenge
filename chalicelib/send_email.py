import os
import json
import boto3
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from botocore.exceptions import ClientError


def send_email(subject, body_message):
    recipient = os.environ['RECIPIENT']

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = os.environ['SENDER']
    msg["To"] = recipient

    # Set message body
    body = MIMEText(body_message, "plain")
    msg.attach(body)

    # Convert message to string and send
    ses_client = boto3.client("ses", region_name=os.environ['AWS_DEFAULT_REGION'])

    ses_client.send_raw_email(
        Source=os.environ['SENDER'],
        Destinations=recipient.split(","),
        RawMessage={"Data": msg.as_string()}
    )

    return True