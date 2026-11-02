import imaplib
import email
import os
import pandas as pd

EMAIL_ID = os.getenv(
    "EMAIL_ID"
)

APP_PASSWORD = os.getenv(
    "APP_PASSWORD"
)

mail = imaplib.IMAP4_SSL(
    "imap.gmail.com",
    993
)

mail.login(
    EMAIL_ID,
    APP_PASSWORD
)

mail.select("INBOX")

_, data = mail.search(
    None,
    "ALL"
)

results = []

for eid in data[0].split():

    try:

        _, msg_data = mail.fetch(
            eid,
            "(RFC822)"
        )

        msg = email.message_from_bytes(
            msg_data[0][1]
        )

        for part in msg.walk():

            filename = (
                part.get_filename()
            )

            if filename:

                results.append({
                    "Sender":
                    msg.get("From"),

                    "Subject":
                    msg.get(
                        "Subject"
                    ),

                    "Attachment":
                    filename
                })

    except:
        pass

df = pd.DataFrame(results)

df.to_csv(
    "reports/emails_with_attachments.csv",
    index=False
)

mail.logout()
