"""
app.py — The Entry Point of Your Backend

This is the "front door" of your entire backend server.
FastAPI listens for HTTP requests and routes them to the right functions.
Think of it as the traffic controller: requests come in, it decides who handles them.

Why FastAPI?
- Auto-generates interactive API docs at /docs (great for demos)
- Very fast, async-friendly
- Clean decorator-based routing (@app.get, @app.post)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.processor import process_email
from services.storage import get_all_emails
from emails.loader import get_random_email

# Create the FastAPI app instance
app = FastAPI(
    title="AI Operations Assistant",
    description="Processes emails using AI and routes them to business workflows",
    version="1.0.0"
)

# ---------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------
# CORS = Cross-Origin Resource Sharing
# Without this, your Next.js frontend (running on port 3000)
# would be BLOCKED from calling your backend (running on port 8000).
# Browsers enforce this security rule by default.
# This middleware tells the browser: "It's okay, I allow it."
# ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check endpoint — confirms the server is running."""
    return {"status": "AI Operations Assistant is running 🚀"}


@app.post("/simulate-email")
def simulate_email():
    """
    POST /simulate-email
    
    Picks a random email from sample_emails.json,
    runs it through the full AI pipeline, saves it,
    and returns the processed record.
    
    Why POST and not GET?
    Because this endpoint CHANGES state (it writes a new record to the DB).
    GET requests should only READ data — that's REST convention.
    """
    try:
        email_text = get_random_email()
        record = process_email(email_text)
        return {"success": True, "record": record}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/emails")
def list_emails():
    """
    GET /emails
    
    Returns all processed email records from db.json.
    The frontend polls this to display the dashboard.
    """
    try:
        emails = get_all_emails()
        return {"success": True, "emails": emails, "count": len(emails)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))