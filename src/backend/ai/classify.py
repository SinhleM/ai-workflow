from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the environment variables specifically for this module
load_dotenv()

# Create the OpenAI client
# It will now find the OPENAI_API_KEY because load_dotenv() ran first
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VALID_INTENTS = {"quote_request", "appointment_change", "invoice_submission"}

def classify_email(email_text: str) -> str:
    """
    Sends the email to GPT-4o-mini and returns one of three intent labels.
    """
    if not os.getenv("OPENAI_API_KEY"):
        print("[Error] No OpenAI API Key found in environment!")
        return "quote_request"

    prompt = f"""Classify the intent of this email into EXACTLY one of these labels:
- quote_request
- appointment_change
- invoice_submission

Email:
{email_text}

Return ONLY the label, nothing else. No explanation, no punctuation."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=50,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.choices[0].message.content.strip().lower()

        if raw in VALID_INTENTS:
            return raw

        for intent in VALID_INTENTS:
            if intent in raw:
                return intent
                
    except Exception as e:
        print(f"[AI Error] Classification failed: {e}")

    return "quote_request"