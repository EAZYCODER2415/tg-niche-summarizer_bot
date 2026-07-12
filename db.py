"""
db.py — MySQL storage layer for the Telegram Summary Bot.

Replaces the in-memory `message_buffer` dict with the highly efficient MySQL storage.
Keeping this in its own module means bot.py doesn't need to know *how*
messages are stored — just that it can call log_message() / get_messages().

Setup:
    pip install mysql-connector-python

    Set these environment variables:
        MYSQL_HOST      (e.g. "localhost")
        MYSQL_USER
        MYSQL_PASSWORD
        MYSQL_DATABASE  (e.g. "telegram_bot")

    Then run init_db() once (bot.py does this automatically on startup)
    to create the messages table if it doesn't exist yet.

--> SUBJECT FOR PERSONAL REVIEW LATER <-- im here
"""

import os
import mysql.connector
from mysql.connector import pooling
from datetime import datetime

# --- Connection pool -------------------------------------------------------
# A pool (rather than one connection reused everywhere) avoids "MySQL server
# has gone away" errors from stale connections, and handles concurrent
# access safely if you later run multiple handlers simultaneously.
_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="bot_pool",
            pool_size=5,
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
        )
    return _pool


def init_db() -> None:
    """Creates the messages table if it doesn't already exist. Call once on startup."""
    conn = _get_pool().get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chat_id BIGINT NOT NULL,
                user VARCHAR(255) NOT NULL,
                text TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                summarized BOOLEAN DEFAULT FALSE,
                INDEX idx_chat_id (chat_id),
                INDEX idx_summarized (summarized)
            )
        """)
        conn.commit()
        cursor.close()
    finally:
        conn.close()


def log_message(chat_id: int, user: str, text: str) -> None:
    """Inserts a single message into the log."""
    conn = _get_pool().get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (chat_id, user, text, timestamp) VALUES (%s, %s, %s, %s)",
            (chat_id, user, text, datetime.utcnow()),
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()


def get_unsummarized_messages(chat_id: int) -> list[dict]:
    """
    Fetches all messages for a chat that haven't been included in a summary yet.
    This is what you'll hand to the LLM in Step 2.
    """
    conn = _get_pool().get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, user, text, timestamp FROM messages "
            "WHERE chat_id = %s AND summarized = FALSE ORDER BY timestamp ASC",
            (chat_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows
    finally:
        conn.close()


def mark_as_summarized(chat_id: int, message_ids: list[int]) -> None:
    """
    Flags messages as summarized after a successful LLM summary, so the next
    /summarize call doesn't reprocess them. Call this after Step 2 runs.
    """
    if not message_ids:
        return
    conn = _get_pool().get_connection()
    try:
        cursor = conn.cursor()
        placeholders = ",".join(["%s"] * len(message_ids))
        cursor.execute(
            f"UPDATE messages SET summarized = TRUE "
            f"WHERE chat_id = %s AND id IN ({placeholders})",
            (chat_id, *message_ids),
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()


def count_unsummarized(chat_id: int) -> int:
    """Handy for the Activity-Based trigger option (e.g. 50+ new messages)."""
    conn = _get_pool().get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM messages WHERE chat_id = %s AND summarized = FALSE",
            (chat_id,),
        )
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    finally:
        conn.close()