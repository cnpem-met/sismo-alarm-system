from enum import Enum, auto
import smtplib, ssl

from config import RECEIVERS_DANGER, RECEIVERS_ALERT
from utils import Severity

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender = "alerta.compactacao@gmail.com"

password = "compactacao123"
message_header = """\
Subject: Alerta Vibracao

"""

def send_email(message: str, severity: Severity) -> None:
    context = ssl.create_default_context()

    email_message = message_header + message

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender, password)

        # select email group that will receive alarm
        if severity == Severity.DANGER:
            receivers = RECEIVERS_DANGER
        elif severity == Severity.ALERT:
            receivers = RECEIVERS_ALERT

        for receiver in receivers:
            server.sendmail(sender, receiver, email_message)

