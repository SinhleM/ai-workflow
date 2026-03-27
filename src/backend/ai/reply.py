"""
ai/reply.py — Step 3 of the AI Pipeline: Automated Response Generation

This module generates a short, professional reply to each incoming email.
This simulates what a real business automation tool would do:
acknowledge receipt automatically, without a human needing to type it.

Why is this valuable for a CV?
It demonstrates you understand LLMs as generative tools,
not just classifiers. You're using them to produce output
that enters the real world (a reply email).
"""

import anthropic

client = anthropic.Anthropic()


def generate_reply(email_text: str, intent: str, extracted_data: dict) -> str:
    """
    Generates a short professional acknowledgment reply.
    
    We pass in both the raw email AND the extracted data.
    This gives Claude richer context so it can personalize the reply
    (e.g., address the customer by name if we extracted it).
    
    Args:
        email_text:     The original email content
        intent:         The classified intent (e.g., "quote_request")
        extracted_data: The structured data we already extracted
        
    Returns:
        A 1-2 sentence professional reply string
    """
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

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=150,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text.strip()