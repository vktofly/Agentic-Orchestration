import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "dspy_jobs.sqlite"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS jobs
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         provider TEXT,
                         status TEXT,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

def add_job(provider: str):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("INSERT INTO jobs (provider, status) VALUES (?, ?)", (provider, 'pending'))
        return cursor.lastrowid

def get_next_job():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        # Get the oldest pending job
        cursor = conn.execute("SELECT id, provider FROM jobs WHERE status = 'pending' ORDER BY created_at ASC LIMIT 1")
        row = cursor.fetchone()
        if row:
            # Mark it as processing
            conn.execute("UPDATE jobs SET status = 'processing' WHERE id = ?", (row[0],))
            return {"id": row[0], "provider": row[1]}
        return None

def complete_job(job_id: int, status: str = 'completed'):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
