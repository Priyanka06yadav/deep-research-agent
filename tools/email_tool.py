
import os
import smtplib

from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_email(
    recipient: str,
    subject: str,
    body: str,
    attachment_path: str
):

    message = EmailMessage()

    message["From"] = os.getenv("SMTP_USERNAME")
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(body)

    # Read the research report
    file_path = Path(attachment_path)

    with open(file_path, "rb") as file:
        file_content = file.read()

    # Attach the report
    message.add_attachment(
        file_content,
        maintype="text",
        subtype="markdown",
        filename=file_path.name
    )

    # Connect to Gmail SMTP server
    with smtplib.SMTP(
        os.getenv("SMTP_HOST"),
        int(os.getenv("SMTP_PORT"))
    ) as server:

        server.starttls()

        server.login(
            os.getenv("SMTP_USERNAME"),
            os.getenv("SMTP_PASSWORD")
        )

        server.send_message(message)

    print("\nEmail sent successfully with research report attached!")
