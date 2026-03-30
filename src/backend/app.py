"""
app.py — The Entry Point of Your Backend
"""

import os
from dotenv import load_dotenv

# 1. Load environment variables FIRST
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 2. Import the "Brain" and "Storage"
# Note: We use simulate_new_email because it handles the random logic + processing
from services.processor import simulate_new_email
from services.storage import get_all_emails

app = FastAPI(
    title="Sinneo AI Operations Assistant",
    description="Processes South African business emails using GPT-4o-mini",
    version="1.0.0"
)

# ---------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "AI Operations Assistant is running 🚀"}

@app.post("/simulate-email")
def simulate_email_endpoint():
    """
    POST /simulate-email
    Triggers the full South African email simulation pipeline.
    """
    try:
        # This function (in processor.py) picks the random email AND processes it
        record = simulate_new_email()
        return {"success": True, "record": record}
    except Exception as e:
        print(f"[Backend Error] Simulation failed: {e}")
        return JSONResponse(
            status_code=500, 
            content={"success": False, "detail": str(e)}
        )

@app.get("/emails")
def list_emails():
    """
    GET /emails
    Returns all processed email records for the Gmail-style dashboard.
    """
    try:
        emails = get_all_emails()
        # Ensure this matches the 'data.emails' expected by your frontend api.ts
        return {"success": True, "emails": emails, "count": len(emails)}
    except Exception as e:
        print(f"[Backend Error] Fetching emails failed: {e}")
        return JSONResponse(
            status_code=500, 
            content={"success": False, "detail": str(e)}
        )