"""
report.py

Creates CSV reports and sender statistics.
"""

import os
import pandas as pd
from collections import Counter


REPORT_FOLDER = "reports"


def create_report_folder():
    os.makedirs(REPORT_FOLDER, exist_ok=True)


def save_email_report(results):

    create_report_folder()

    df = pd.DataFrame(results)

    path = f"{REPORT_FOLDER}/email_report.csv"

    df.to_csv(path, index=False)

    print(f"Report saved: {path}")


def save_category_summary(results):

    summary = Counter(
        item["category"]
        for item in results
    )

    df = pd.DataFrame(
        summary.items(),
        columns=[
            "Category",
            "Count"
        ]
    )

    path = (
        f"{REPORT_FOLDER}/"
        "category_summary.csv"
    )

    df.to_csv(path, index=False)

    print(f"Saved: {path}")


def save_sender_summary(sender_counter):

    df = pd.DataFrame(
        sender_counter.items(),
        columns=[
            "Sender",
            "Count"
        ]
    )

    path = (
        f"{REPORT_FOLDER}/"
        "top_senders.csv"
    )

    df.to_csv(path, index=False)

    print(f"Saved: {path}")
