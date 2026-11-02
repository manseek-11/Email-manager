import email
import imaplib
import os

from email.header import decode_header
from collections import Counter

from classify import categorize
from report import (
    save_email_report,
    save_category_summary,
    save_sender_summary
)

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

MAX_EMAILS = int(
    os.getenv("MAX_EMAILS", "500")
)


def decode_text(text):

    try:

        decoded = decode_header(text)[0]

        if isinstance(decoded[0], bytes):

            return decoded[0].decode(
                decoded[1]
                if decoded[1]
                else "utf-8",
                errors="ignore"
            )

        return decoded[0]

    except:
        return text


def get_body(msg):

    body = ""

    try:

        if msg.is_multipart():

            for part in msg.walk():

                if (
                    part.get_content_type()
                    == "text/plain"
                ):

                    payload = part.get_payload(
                        decode=True
                    )

                    if payload:
                        body = payload.decode(
                            errors="ignore"
                        )

                        break

        else:

            payload = msg.get_payload(
                decode=True
            )

            if payload:

                body = payload.decode(
                    errors="ignore"
                )

    except:
        pass

    return body[:5000]


def main():

    email_id = os.getenv(
        "EMAIL_ID"
    )

    password = os.getenv(
        "APP_PASSWORD"
    )

    mail = imaplib.IMAP4_SSL(
        IMAP_SERVER,
        IMAP_PORT
    )

    mail.login(
        email_id,
        password
    )

    mail.select(
        "INBOX"
    )

    _, data = mail.search(
        None,
        "ALL"
    )

    ids = data[0].split()

    ids = ids[-MAX_EMAILS:]

    results = []

    sender_counter = Counter()

    for eid in reversed(ids):

        try:

            _, msg_data = mail.fetch(
                eid,
                "(RFC822)"
            )

            raw = msg_data[0][1]

            msg = (
                email
                .message_from_bytes(raw)
            )

            subject = decode_text(
                msg.get(
                    "Subject",
                    ""
                )
            )

            sender = decode_text(
                msg.get(
                    "From",
                    ""
                )
            )

            body = get_body(msg)

            category = categorize(
                subject,
                sender,
                body
            )

            sender_counter[
                sender
            ] += 1

            results.append(
                {
                    "id": eid.decode(),
                    "subject": subject,
                    "sender": sender,
                    "category": category
                }
            )

        except Exception as ex:

            print(ex)

    save_email_report(results)

    save_category_summary(results)

    save_sender_summary(
        sender_counter
    )

    mail.logout()


if __name__ == "__main__":
    main()
