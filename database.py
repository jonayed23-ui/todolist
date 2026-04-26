"""
database.py — SQLite handler for VIVID app
All data is stored in data/vivid.db
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "vivid.db")


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Initialize database tables and seed sample data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = _connect()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            text       TEXT NOT NULL,
            category   TEXT DEFAULT 'Work',
            done       INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT NOT NULL,
            body       TEXT,
            color      TEXT DEFAULT '#FF3399',
            created_at TEXT
        )
    """)

    # Seed sample tasks
    c.execute("SELECT COUNT(*) FROM tasks")
    if c.fetchone()[0] == 0:
        seeds = [
            ("Review Q3 project proposal",    "Work",     0),
            ("30 min morning run",             "Health",   0),
            ("Buy groceries for the week",     "Personal", 0),
            ("Sketch logo concepts",           "Creative", 1),
            ("Finish API integration PR",      "Work",     0),
            ("Book dentist appointment",       "Health",   1),
        ]
        for text, cat, done in seeds:
            c.execute(
                "INSERT INTO tasks (text, category, done, created_at) VALUES (?,?,?,?)",
                (text, cat, done, _today())
            )

    # Seed sample notes
    c.execute("SELECT COUNT(*) FROM notes")
    if c.fetchone()[0] == 0:
        seeds = [
            ("Brand Brainstorm",  "Bold type + flat colors. Avoid gradients — flat is modern.",  "#FF3399"),
            ("Book List",         "Atomic Habits, Deep Work, The Creative Act — must reads.",    "#00C8E0"),
            ("Weekly Goals",      "1. Finish app  2. Morning runs  3. Read 30 min/day",          "#2BB84A"),
            ("Project Ideas",     "Habit tracker, AI recipe app, Open source UI kit",            "#D4B800"),
        ]
        for title, body, color in seeds:
            c.execute(
                "INSERT INTO notes (title, body, color, created_at) VALUES (?,?,?,?)",
                (title, body, color, _date_label())
            )

    conn.commit()
    conn.close()


# ── TASKS ────────────────────────────────────────────────────

def get_tasks(category=None):
    """Return all tasks, optionally filtered by category."""
    conn = _connect()
    c = conn.cursor()
    if category and category not in ("All", "Done"):
        c.execute(
            "SELECT id, text, category, done, created_at FROM tasks "
            "WHERE category=? ORDER BY done ASC, id DESC",
            (category,)
        )
    else:
        c.execute(
            "SELECT id, text, category, done, created_at FROM tasks "
            "ORDER BY done ASC, id DESC"
        )
    rows = c.fetchall()
    conn.close()
    return rows


def add_task(text, category):
    conn = _connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (text, category, done, created_at) VALUES (?,?,0,?)",
        (text, category, _today())
    )
    conn.commit()
    conn.close()


def toggle_task(task_id):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE tasks SET done = CASE WHEN done=0 THEN 1 ELSE 0 END WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = _connect()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


# ── NOTES ────────────────────────────────────────────────────

def get_notes():
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT id, title, body, color, created_at FROM notes ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def add_note(title, body, color):
    conn = _connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO notes (title, body, color, created_at) VALUES (?,?,?,?)",
        (title, body, color, _date_label())
    )
    conn.commit()
    conn.close()


def delete_note(note_id):
    conn = _connect()
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()


# ── STATS ────────────────────────────────────────────────────

def get_stats():
    """Return (total_tasks, done_tasks)."""
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tasks")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE done=1")
    done = c.fetchone()[0]
    conn.close()
    return total, done


# ── HELPERS ──────────────────────────────────────────────────

def _today():
    return datetime.now().strftime("%Y-%m-%d")


def _date_label():
    return datetime.now().strftime("%b %d")
