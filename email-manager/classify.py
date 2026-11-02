"""
classify.py

Contains all email classification rules and helper functions.
"""

CATEGORY_RULES = {
    "Salary": [
        "salary credited",
        "payroll",
        "salary account"
    ],

    "Banking": [
        "upi",
        "credited",
        "debited",
        "transaction",
        "withdrawal",
        "deposit",
        "account balance"
    ],

    "Credit Card": [
        "credit card",
        "statement",
        "minimum due",
        "payment due"
    ],

    "Investment": [
        "mutual fund",
        "sip",
        "zerodha",
        "groww",
        "investment",
        "stocks"
    ],

    "Jobs": [
        "interview",
        "job",
        "recruiter",
        "application",
        "hiring"
    ],

    "LinkedIn": [
        "linkedin"
    ],

    "GitHub": [
        "github"
    ],

    "Learning": [
        "coursera",
        "udemy",
        "microsoft learn",
        "exam",
        "certification"
    ],

    "Shopping": [
        "amazon",
        "flipkart",
        "order delivered",
        "order shipped"
    ],

    "Travel": [
        "flight",
        "boarding pass",
        "hotel",
        "trip"
    ],

    "Newsletter": [
        "unsubscribe",
        "newsletter",
        "daily digest",
        "weekly digest"
    ],

    "Promotion": [
        "offer",
        "discount",
        "sale",
        "coupon"
    ],

    "Social": [
        "facebook",
        "instagram",
        "twitter",
        "x.com"
    ],
    "Protected": [
        "rws",
        "trainai",
        "train ai",
        "rws group",
        "rws holdings",
        "ai testing",
        "linguistic testing",
        "assessment",
        "language assessment"
    ]
}


def categorize(subject, sender, body):
    """
    Categorize email using keyword matching.
    """

    content = f"{subject} {sender} {body}".lower()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword.lower() in content:
                return category

    return "Others"
