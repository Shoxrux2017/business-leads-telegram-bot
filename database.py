import sqlite3
from datetime import datetime


def init_db(database_path: str) -> None:
    with sqlite3.connect(database_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                telegram_user_id INTEGER,
                telegram_username TEXT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT NOT NULL,
                comment TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_lead(
    database_path: str,
    telegram_user_id: int | None,
    telegram_username: str | None,
    name: str,
    phone: str,
    service: str,
    comment: str,
) -> int:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(database_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO leads (
                created_at,
                telegram_user_id,
                telegram_username,
                name,
                phone,
                service,
                comment
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                telegram_user_id,
                telegram_username,
                name,
                phone,
                service,
                comment,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)