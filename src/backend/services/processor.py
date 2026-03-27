"""
services/processor.py — The Orchestrator / Brain of the Backend

This is the most important file in your backend.
It doesn't DO any one thing — it COORDINATES everything.

Think of it like a factory assembly line manager:
1. Receive raw email
2. Send to AI for classification
3. Send to AI for data extraction
4. Determine which department it belongs to
5. Send to AI for reply generation
6. Build the final record
7. Save to storage
8. Return the record

Why separate this from app.py?
app.py handles HTTP. processor.py handles BUSINESS LOGIC.
This separation means you could call process_email() from a CLI,
a cron job, a Celery task, or a webhook — not just an HTTP endpoint.
"""

import uuid
from datetime import datetime

from ai.classify import classify_email
from ai.extract import extract_data
from ai.reply import generate_reply
from services.storage import save_email


# ---------------------------------------------------------------
# Routing Table: Intent → Department
# ---------------------------------------------------------------
# This is your "Workflow Automation Engine".
# In a real system, this could trigger Slack notifications,
# create CRM entries, or send calendar invites.
# Here we keep it simple: assign a department label.
# ---------------------------------------------------------------
DEPARTMENT_MAP = {
    "quote_request":       "sales",
    "appointment_change":  "calendar",
    "invoice_submission":  "finance"
}


def route_to_department(intent: str) -> str:
    """Maps an intent label to a business department."""
    return DEPARTMENT_MAP.get(intent, "general")


def process_email(email_text: str) -> dict:
    """
    Full AI processing pipeline for a single email.
    
    This function is intentionally sequential (not async) for clarity.
    Each step depends on the previous, so parallelism doesn't help here.
    
    Args:
        email_text: Raw email string
        
    Returns:
        Complete processed record dict (also saved to db.json)
    """
    
    # --- Step 1: Classify Intent ---
    # "What does this person want?"
    print(f"[Processor] Step 1: Classifying email...")
    intent = classify_email(email_text)
    print(f"[Processor] → Intent: {intent}")

    # --- Step 2: Extract Structured Data ---
    # "Who sent it? What are the details?"
    print(f"[Processor] Step 2: Extracting data...")
    extracted = extract_data(email_text)
    print(f"[Processor] → Extracted: {extracted}")

    # --- Step 3: Route to Department ---
    # Pure Python logic — no AI needed here
    department = route_to_department(intent)
    print(f"[Processor] → Department: {department}")

    # --- Step 4: Generate Reply ---
    # "How do we acknowledge this email professionally?"
    print(f"[Processor] Step 3: Generating reply...")
    reply = generate_reply(email_text, intent, extracted)
    print(f"[Processor] → Reply generated")

    # --- Step 5: Build the Final Record ---
    # This is what gets stored and displayed on the dashboard
    record = {
        "id": str(uuid.uuid4()),             # Unique ID for each record
        "timestamp": datetime.utcnow().isoformat() + "Z",  # ISO 8601 timestamp
        "email": email_text,                  # Original email text
        "intent": intent,                     # Classified label
        "department": department,             # Routed department
        "extracted_data": extracted,          # Structured fields
        "response": reply,                    # AI-generated reply
        "status": "processed"                 # Could be: pending, processed, failed
    }

    # --- Step 6: Persist ---
    save_email(record)
    print(f"[Processor] ✅ Record saved: {record['id']}")

    return record