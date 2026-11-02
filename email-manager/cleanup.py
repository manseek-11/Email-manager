"""
Delete emails by category.
"""

import os
import email
import imaplib

from classify import categorize

PROTECTED_CATEGORIES = [
    "Protected"
]

if CATEGORY in PROTECTED_CATEGORIES:
    raise Exception(
        "Protected category cannot be deleted."
    )

EMAIL_ID = os.getenv("EMAIL_ID")
APP_PASSWORD = os.getenv("APP_PASSWORD")
CATEGORY = os.getenv("CATEGORY")

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

for eid in data[0].split():

    try:

        _, msg_data = mail.fetch(
            eid,
            "(RFC822)"
        )

        msg = email.message_from_bytes(
            msg_data[0][1]
        )

        subject = (
            msg.get(
                "Subject",
                ""
            )
        )

        sender = (
            msg.get(
                "From",
                ""
            )
        )

        category = categorize(
            subject,
            sender,
            ""
        )

        if (
            category.lower()
            ==
            CATEGORY.lower()
        ):

            mail.store(
                eid,
                "+FLAGS",
                "\\Deleted"
            )

    except:
        pass

mail.expunge()

mail.logout()

print(
    f"Deleted all emails "
    f"in category "
    f"{CATEGORY}"
)
