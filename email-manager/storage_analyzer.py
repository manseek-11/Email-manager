import imaplib
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

email_count = 0
total_size = 0

for eid in data[0].split():

    try:

        _, msg_data = mail.fetch(
            eid,
            "(RFC822)"
        )

        raw_email = (
            msg_data[0][1]
        )

        total_size += len(raw_email)

        email_count += 1

    except:
        pass

report = pd.DataFrame(
    [
        {
            "Total Emails":
            email_count,

            "Approx Size MB":
            round(
                total_size
                /
                1024
                /
                1024,
                2
            )
        }
    ]
)

report.to_csv(
    "reports/storage_report.csv",
    index=False
)

mail.logout()
