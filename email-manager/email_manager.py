import email
import imaplib
import os

from email.header import decode_header
from collections import Counter

from classify import categorize
from report import (
    save_email_report,
    save_category_summary,
    save_sender_summary,
    save_mailbox_stats
)

# ==========================================
# Gmail Configuration
# ==========================================

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

MAX_EMAILS = int(
    os.getenv("MAX_EMAILS", "500")
)


# ==========================================
# Decode Email Headers
# ==========================================

def decode_text(text):

    try:

        if not text:
            return ""

        decoded = decode_header(text)[0]

        if isinstance(decoded[0], bytes):

            return decoded[0].decode(
                decoded[1]
                if decoded[1]
                else "utf-8",
                errors="ignore"
            )

        return decoded[0]

    except Exception:
        return str(text)


# ==========================================
# Extract Email Body
# ==========================================

def get_body(msg):

    body = ""

    try:

        if msg.is_multipart():

            for part in msg.walk():

                content_type = (
                    part.get_content_type()
                )

                content_disposition = str(
                    part.get(
                        "Content-Disposition"
                    )
                )

                if (
                    content_type == "text/plain"
                    and "attachment"
                    not in content_disposition.lower()
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

    except Exception:
        pass

    return body[:5000]


# ==========================================
# Main Program
# ==========================================

def main():

    email_id = os.getenv(
        "EMAIL_ID"
    )

    password = os.getenv(
        "APP_PASSWORD"
    )

    if not email_id or not password:

        raise Exception(
            "EMAIL_ID or APP_PASSWORD not provided."
        )

    print("\nConnecting to Gmail...")

    mail = imaplib.IMAP4_SSL(
        IMAP_SERVER,
        IMAP_PORT
    )

    mail.login(
        email_id,
        password
    )

    print("Login successful.")

    mail.select(
        "INBOX"
    )

    status, data = mail.search(
        None,
        "ALL"
    )

    if status != "OK":

        raise Exception(
            "Unable to read mailbox."
        )

    all_ids = data[0].split()

    # Total emails currently present in mailbox
    total_mail_count = len(
        all_ids
    )

    print(
        f"\nTotal Emails In Inbox: "
        f"{total_mail_count}"
    )

    # Limit scan count
    ids = all_ids[-MAX_EMAILS:]

    print(
        f"Scanning latest "
        f"{len(ids)} emails..."
    )

    results = []

    sender_counter = Counter()

    category_counter = Counter()

    scanned_count = 0

    for eid in reversed(ids):

        try:

            _, msg_data = mail.fetch(
                eid,
                "(RFC822)"
            )

            raw_email = msg_data[0][1]

            msg = (
                email.message_from_bytes(
                    raw_email
                )
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

            body = get_body(
                msg
            )

            category = categorize(
                subject,
                sender,
                body
            )

            sender_counter[
                sender
            ] += 1

            category_counter[
                category
            ] += 1

            results.append(
                {
                    "id":
                    eid.decode(),

                    "subject":
                    subject,

                    "sender":
                    sender,

                    "category":
                    category
                }
            )

            scanned_count += 1

        except Exception as ex:

            print(
                f"Error processing email: {ex}"
            )

    # ==========================================
    # Save Reports
    # ==========================================

    save_email_report(
        results
    )

    save_category_summary(
        results
    )

    save_sender_summary(
        sender_counter
    )

    save_mailbox_stats(
        total_mail_count,
        scanned_count,
        len(sender_counter)
    )

    # ==========================================
    # Print Summary
    # ==========================================

    print(
        "\n=================================="
    )

    print(
        f"Total Inbox Emails : "
        f"{total_mail_count}"
    )

    print(
        f"Emails Scanned     : "
        f"{scanned_count}"
    )

    print(
        f"Unique Senders     : "
        f"{len(sender_counter)}"
    )

    print(
        "\nCategory Summary"
    )

    print(
        "---------------------------"
    )

    for category, count in (
        category_counter.most_common()
    ):

        print(
            f"{category:<20} {count}"
        )

    print(
        "\nReports Generated"
    )

    print(
        "- reports/email_report.csv"
    )

    print(
        "- reports/category_summary.csv"
    )

    print(
        "- reports/top_senders.csv"
    )

    print(
        "- reports/mailbox_stats.csv"
    )

    print(
        "=================================="
    )

    mail.logout()

    print(
        "\nCompleted Successfully."
    )


# ==========================================
# Entry Point
# ==========================================

if __name__ == "__main__":
    main()
