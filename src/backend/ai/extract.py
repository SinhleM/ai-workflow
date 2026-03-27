"""
ai/extract.py — Step 2 of the AI Pipeline: Structured Data Extraction

This is where the "magic" happens visually — unstructured text becomes
clean, machine-readable JSON.

Why does this matter?
An email like: "Hi, I'm John and I need a quote for 10 desks by Friday"
becomes: { "customer_name": "John", "details": "10 desks", "date": "Friday" }

That structured data is what allows automation. You can't build workflows
on raw text — you CAN build them on structured fields.
"""

import json
import anthropic

client = anthropic.Anthropic()


def extract_data(email_text: str) -> dict:
    """
    Extracts key structured fields from a raw email using Claude.
    
    Why ask for JSON specifically?
    Because we need to parse the response programmatically.
    We also add "Return ONLY valid JSON" to prevent markdown code fences
    (Claude sometimes wraps JSON in ```json ... ``` blocks).
    
    Args:
        email_text: The raw email content
        
    Returns:
        Dict with keys: customer_name, intent, details, date
    """
    prompt = f"""Extract structured data from this email.

Return ONLY valid JSON (no markdown, no explanation) in exactly this format:
{{
  "customer_name": "extracted name or null",
  "intent": "what they want",
  "details": "key details about the request",
  "date": "any date mentioned or null"
}}

Email:
{email_text}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = message.content[0].text.strip()

    # ---------------------------------------------------------------
    # Robust JSON Parsing
    # ---------------------------------------------------------------
    # LLMs sometimes return: ```json { ... } ```
    # We strip the markdown fences before parsing.
    # This is a common real-world defensive pattern.
    # ---------------------------------------------------------------
    if raw.startswith("```"):
        lines = raw.split("\n")
        # Remove first line (```json) and last line (```)
        raw = "\n".join(lines[1:-1])

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # If parsing fails, return a safe default
        return {
            "customer_name": None,
            "intent": "unknown",
            "details": email_text[:100],  # First 100 chars as fallback
            "date": None
        }