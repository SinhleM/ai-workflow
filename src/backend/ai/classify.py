"""
ai/classify.py — Step 1 of the AI Pipeline: Intent Classification

This module's ONLY job is to figure out WHY someone sent an email.
It sends the email text to the LLM and gets back a single label.

Why is this its own file?
Single Responsibility Principle — each file does ONE thing.
If you later want to swap Anthropic for OpenAI, you only change THIS file.
The rest of your app doesn't care HOW the classification happens.
"""

import anthropic

# Create the Anthropic client once (reused across calls)
# It automatically reads the ANTHROPIC_API_KEY environment variable
client = anthropic.Anthropic()

# The three intents our system understands
VALID_INTENTS = {"quote_request", "appointment_change", "invoice_submission"}


def classify_email(email_text: str) -> str:
    """
    Sends the email to Claude and returns one of three intent labels.
    
    Why "Return ONLY the label"?
    LLMs love to be chatty ("Sure! The intent is: quote_request. Let me explain...").
    By being strict in the prompt, we get a clean string we can use directly.
    
    Args:
        email_text: The raw email content
        
    Returns:
        One of: "quote_request", "appointment_change", "invoice_submission"
    """
    prompt = f"""Classify the intent of this email into EXACTLY one of these labels:
- quote_request
- appointment_change
- invoice_submission

Email:
{email_text}

Return ONLY the label, nothing else. No explanation, no punctuation."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=50,  # We only need a few words back
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the text from the response
    raw = message.content[0].text.strip().lower()

    # Validate — if the LLM goes rogue, fall back gracefully
    if raw in VALID_INTENTS:
        return raw
    
    # If the response contains a valid intent (e.g., "I think it's quote_request")
    for intent in VALID_INTENTS:
        if intent in raw:
            return intent
    
    # Default fallback
    return "quote_request"