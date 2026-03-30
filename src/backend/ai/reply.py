import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

# Create the OpenAI client
# It will now find the key because load_dotenv() ran first
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(email_text: str, intent: str, extracted_data: dict) -> str:
    """
    Generates a short professional acknowledgment reply using GPT-4o-mini.
    """
    # Safety check for the API key
    if not os.getenv("OPENAI_API_KEY"):
        print("[Error] No OpenAI API Key found for reply generation!")
        return "Thank you for your email. Our team has received your request and will get back to you shortly."

    customer_name = extracted_data.get("customer_name") or "there"

    # Map intents to human-readable descriptions for the prompt
    intent_descriptions = {
        "quote_request": "quote request",
        "appointment_change": "appointment change request",
        "invoice_submission": "invoice submission"
    }
    intent_label = intent_descriptions.get(intent, "request")

    prompt = f"""Write a short, professional email reply acknowledging receipt of this {intent_label}.

Address the customer as "{customer_name}".
Keep it to 2 sentences maximum.
Be warm but concise.
Do NOT say "I" — write from the company's perspective (use "We" or "Our team").

Original email:
{email_text}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=150,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[AI Error] Reply generation failed: {e}")
        return f"Hello {customer_name}, thank you for reaching out. We have received your {intent_label} and will process it shortly."