import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

# Create the OpenAI client
# It will now find the key because load_dotenv() ran first
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_data(email_text: str) -> dict:
    """
    Extracts key structured fields from a raw email using GPT-4o-mini.
    """
    # Safety check for the API key
    if not os.getenv("OPENAI_API_KEY"):
        print("[Error] No OpenAI API Key found for extraction!")
        return {
            "customer_name": None,
            "intent": "unknown",
            "details": email_text[:50],
            "date": None
        }

    prompt = f"""Extract structured data from this email.

Return ONLY valid JSON in exactly this format:
{{
  "customer_name": "extracted name or null",
  "intent": "what they want",
  "details": "key details about the request",
  "date": "any date mentioned or null"
}}

Email:
{email_text}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=300,
            # response_format forces OpenAI to return valid JSON
            response_format={"type": "json_object"},
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.choices[0].message.content.strip()
        return json.loads(raw)

    except (json.JSONDecodeError, Exception) as e:
        print(f"[AI Error] Extraction failed: {e}")
        # Fallback in case something unexpected happens
        return {
            "customer_name": None,
            "intent": "error",
            "details": email_text[:100],
            "date": None
        }