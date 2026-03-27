"""
emails/loader.py — Email Simulator

This module simulates an email inbox by randomly picking
from a predefined set of emails stored in sample_emails.json.

Why simulate emails instead of connecting to a real inbox?
1. No email credentials needed
2. Controlled, predictable test data
3. Can demo the system without a live email account
4. Covers all 3 intent types so you can test every workflow path

In production, you'd replace get_random_email() with
a function that polls Gmail/Outlook via their APIs.
The rest of your pipeline wouldn't change at all.
"""

import json
import random
from pathlib import Path

# Path to the sample emails file
EMAILS_PATH = Path(__file__).parent / "sample_emails.json"


def get_all_sample_emails() -> list:
    """Loads and returns all sample emails from JSON."""
    with open(EMAILS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_random_email() -> str:
    """
    Returns the body text of a randomly selected sample email.
    
    Why return just the body as a string (not the whole object)?
    Because our AI pipeline only needs the text content.
    The ID and subject from sample_emails.json are just for organisation.
    When a real email arrives, you'd extract the body and pass it in the same way.
    """
    emails = get_all_sample_emails()
    selected = random.choice(emails)
    return selected["body"]