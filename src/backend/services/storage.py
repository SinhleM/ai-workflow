import json
import os
from pathlib import Path
from typing import List  # <--- This was missing and caused the crash!

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "db.json"

def _ensure_db_exists():
    """Ensures the directory and file exist with valid JSON."""
    try:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not DB_PATH.exists() or DB_PATH.stat().st_size == 0:
            with open(DB_PATH, "w", encoding="utf-8") as f:
                f.write("[]")
    except Exception as e:
        print(f"[Storage Error] Could not ensure DB exists: {e}")

def _read_db() -> List[dict]:
    """Reads and parses the entire db.json file."""
    _ensure_db_exists()
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            return json.loads(content) if content.strip() else []
    except (json.JSONDecodeError, Exception) as e:
        print(f"[Storage Error] Failed to read JSON: {e}")
        return []

def _write_db(records: List[dict]):
    """Writes the full records list back to db.json."""
    _ensure_db_exists()
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def save_email(record: dict):
    records = _read_db()
    records.append(record)
    _write_db(records)

def get_all_emails() -> List[dict]:
    records = _read_db()
    # Return reversed list (newest first)
    return records[::-1] 

def clear_all_emails():
    _write_db([])