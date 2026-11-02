import imaplib
import email
import os

EMAIL_ID = os.getenv(
    "EMAIL_ID"
)

APP_PASSWORD = os.getenv(
    "APP_PASSWORD"
)

DOMAIN = os.getenv(
    "DOMAIN"
)

mail = imaplib.IMAP4_SSL(
    "imap.gmail.com",
    993
)

mail.login(
    EMAIL_ID,
    APP_PASSWORD
)

mail.select(
    "INBOX"
)

_, data = mail.search(
    None,
    "ALL"
)

deleted = 0

for eid in data[0].split():

    try:

        _, msg_data = mail.fetch(
            eid,
            "(RFC822)"
        )

        msg = (
            email
            .message_from_bytes(
                msg_data[0][1]
            )
        )

        sender = (
            msg.get(
                "From",
                ""
            )
        )

        if DOMAIN.lower() in sender.lower():

            mail.store(
                eid,
                "+FLAGS",
                "\\Deleted"
            )

            deleted += 1

    except:
        pass

mail.expunge()

mail.logout()

print(
    f"Deleted {deleted} emails"
)
