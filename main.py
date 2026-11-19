import imaplib
import email
import os
import time
from email.header import decode_header

import pywhatkit
from dotenv import load_dotenv

load_dotenv()

GMAIL = os.getenv("GMAIL_ADDRESS")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
MY_WHATSAPP = os.getenv("MY_WHATSAPP")


def decode_text(value):
    """Convert encoded email headers into readable text."""
    if not value:
        return ""
    result = ""
    for part, encoding in decode_header(value):
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="ignore")
        else:
            result += part
    return result


def send_whatsapp(text):
    pywhatkit.sendwhatmsg_instantly(
        MY_WHATSAPP, text, wait_time=15, tab_close=True, close_time=3
    )


def check_new_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL, APP_PASSWORD)
    mail.select("inbox")

    status, data = mail.search(None, "UNSEEN")
    for num in data[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        sender = decode_text(msg["From"])
        subject = decode_text(msg["Subject"])

        send_whatsapp(f"New email\nFrom: {sender}\nSubject: {subject}")
        print("Notified:", subject)

    mail.logout()


if __name__ == "__main__":
    print("Email notifier started...")
    while True:
        try:
            check_new_emails()
        except Exception as error:
            print("Error:", error)
        time.sleep(60)  # check every 60 seconds