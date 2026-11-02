import pandas as pd
from collections import Counter

def save_domain_report(results):

    domains = []

    for item in results:

        sender = item["sender"]

        try:
            domain = sender.split("@")[1]

            if ">" in domain:
                domain = domain.split(">")[0]

            domains.append(
                domain.lower()
            )

        except:
            pass

    counter = Counter(domains)

    df = pd.DataFrame(
        counter.items(),
        columns=[
            "Domain",
            "Count"
        ]
    )

    df.sort_values(
        "Count",
        ascending=False
    ).to_csv(
        "reports/top_domains.csv",
        index=False
    )
