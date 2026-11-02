import imaplib
import email
import os
import pandas as pd
from datetime import datetime, timedelta

EMAIL_ID = os.getenv("EMAIL_ID")
APP_PASSWORD = os.getenv("APP_PASSWORD")

DAYS = int(
    os.getenv("DAYS", "365")
)

cutoff = (
    datetime.now()
    - timedelta(days=DAYS)
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

result, data = mail.search(
    None,
    "UNSEEN"
)

emails = []

for eid in data[0].split():

    try:

        _, msg_data = mail.fetch(
            eid,
            "(RFC822)"
        )

        msg = email.message_from_bytes(
            msg_data[0][1]
        )

        date_str = msg["Date"]

        emails.append({
            "Subject":
            msg.get("Subject"),
            "Sender":
            msg.get("From"),
            "Date":
            date_str
        })

    except:
        pass

df = pd.DataFrame(emails)

df.to_csv(
    "reports/old_unread.csv",
    index=False
)

mail.logout()
