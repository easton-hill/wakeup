from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl

def send(html, subject, to):
    """
    Sends an email with plain text and HTML content using gmail SMTP server

        Parameters:
            html (string):    The HTML content (plain text will be crated using an HTML parser)
            subject (string): Subject of the email
            to (string):      Email address that will receive the email
    """

    # use gmail smtp server
    port = 465
    smtp_server = "smtp.gmail.com"

    # email account to send from, user/password stored in environment variables
    sender = os.environ["MAIL_USER"]
    password = os.environ["MAIL_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    text = BeautifulSoup(html, "html.parser").text.strip()
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, to, msg.as_string())