import email
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

        unsubscribe_link = (
            msg.get(
                "List-Unsubscribe"
            )
        )

        if unsubscribe_link:

            results.append(
                {
                    "Sender":
                    msg.get("From"),

                    "Subject":
                    msg.get(
                        "Subject"
                    ),

                    "Unsubscribe":
                    unsubscribe_link
                }
            )

    except:
        pass

df = pd.DataFrame(results)

df.to_csv(
    "reports/unsubscribe_candidates.csv",
    index=False
)

mail.logout()
