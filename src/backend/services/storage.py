"""
services/storage.py — Your "Database" Layer

This file handles all reading and writing to db.json.
It's intentionally simple — a JSON file acting as a database.

Why JSON instead of a real DB?
For rapid prototyping and demos, JSON storage means:
- Zero setup (no Postgres, no Docker, no ORM)
- Human-readable (open the file and see your data)
- Portable (copy the file and take your data with you)

In production you'd swap this with PostgreSQL + SQLAlchemy,
but the INTERFACE stays the same — that's the point of this abstraction layer.
The rest of your code calls save_email() and get_all_emails() and
doesn't care how the data is stored underneath.
"""

import json
import os
from pathlib import Path
from typing import List

# ---------------------------------------------------------------
# Path Resolution
# ---------------------------------------------------------------
# __file__ = the path to THIS file (storage.py)
# .parent   = the services/ folder
# .parent   = the backend/ folder
# / "data/db.json" = our target file
# Using Path ensures this works on Windows AND Mac/Linux
# ---------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "db.json"


def _ensure_db_exists():
    """
    Creates db.json with an empty array if it doesn't exist yet.
    Called before every read/write to prevent FileNotFoundError.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Create data/ folder if needed
    if not DB_PATH.exists():
        DB_PATH.write_text("[]")  # Empty JSON array


def _read_db() -> List[dict]:
    """Reads and parses the entire db.json file."""
    _ensure_db_exists()
    content = DB_PATH.read_text(encoding="utf-8")
    return json.loads(content)


def _write_db(records: List[dict]):
    """
    Writes the full records list back to db.json.
    
    indent=2 makes the JSON human-readable (pretty-printed).
    ensure_ascii=False preserves special characters (é, ü, etc.)
    """
    DB_PATH.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def save_email(record: dict):
    """
    Appends a new processed email record to the database.
    
    Read → Append → Write
    This is safe for our single-server prototype.
    (In production with concurrent requests, you'd use transactions.)
    """
    records = _read_db()
    records.append(record)
    _write_db(records)


def get_all_emails() -> List[dict]:
    """
    Returns all processed email records, newest first.
    
    Why reverse? The dashboard shows most recent at the top,
    which is the most natural UX for an inbox-style view.
    """
    records = _read_db()
    return list(reversed(records))  # Newest first


def clear_all_emails():
    """
    Utility function to reset the database.
    Useful during development and testing.
    """
    _write_db([])