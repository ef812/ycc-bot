# -*- coding: utf-8 -*-
"""SQLite storage layer for YCC membership registrations."""
import sqlite3
import csv
import io
import os
from contextlib import contextmanager
from datetime import datetime

# Configurable so a persistent volume (e.g. on Railway) can be mounted
# somewhere and pointed at via this env var. Defaults to local ./data
# for plain local runs.
DB_PATH = os.environ.get("YCC_DB_PATH", "data/ycc.db")
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS members (
    telegram_id INTEGER PRIMARY KEY,
    full_name   TEXT NOT NULL,
    phone       TEXT NOT NULL,
    school      TEXT NOT NULL,
    grade       INTEGER NOT NULL,
    photo_file_id TEXT NOT NULL,
    language    TEXT NOT NULL DEFAULT 'en',
    joined_at   TEXT NOT NULL
);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute(SCHEMA)


def is_registered(telegram_id: int) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM members WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        return row is not None


def get_member(telegram_id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM members WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        return dict(row) if row else None


def add_member(telegram_id: int, full_name: str, phone: str, school: str,
                grade: int, photo_file_id: str, language: str):
    with get_conn() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO members
               (telegram_id, full_name, phone, school, grade, photo_file_id, language, joined_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (telegram_id, full_name, phone, school, grade, photo_file_id,
             language, datetime.utcnow().isoformat()),
        )


def delete_member(telegram_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM members WHERE telegram_id = ?", (telegram_id,))
        return cur.rowcount > 0


def count_members() -> int:
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) AS c FROM members").fetchone()["c"]


def all_members():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM members ORDER BY joined_at").fetchall()
        return [dict(r) for r in rows]


def export_csv() -> io.BytesIO:
    """Export all members to an in-memory CSV file."""
    members = all_members()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["telegram_id", "full_name", "phone", "school", "grade",
                      "language", "joined_at"])
    for m in members:
        writer.writerow([m["telegram_id"], m["full_name"], m["phone"],
                          m["school"], m["grade"], m["language"], m["joined_at"]])
    bio = io.BytesIO(buf.getvalue().encode("utf-8-sig"))
    bio.name = "ycc_members.csv"
    return bio
