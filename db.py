"""
db.py — SQLite database layer for the Telegram Summary Bot.

Replaces the in-memory `message_buffer` dict with SQLite commands.
This is a Python library using the SQLite module, to process and store messages
in a SQLite database from Telegram handlers.

"""

import sqlite3
from datetime import datetime, timedelta, timezone

def init_db():
    """Initialize the SQLite database and create the messages table if it doesn't exist."""
    with sqlite3.connect("messages.db") as conn:
        conn.row_factory = sqlite3.Row # prevent numerical index positions, so use dicts instead
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                chat_type TEXT NOT NULL,
                thread_id INTEGER,
                chat_title TEXT,
                user TEXT NOT NULL,
                text TEXT NOT NULL,
                has_attachment BOOLEAN DEFAULT 0,
                attachment_type TEXT,
                file_id TEXT,
                file_name TEXT,
                local_path TEXT,
                mime_type TEXT,
                file_size INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

def log_message(
        chat_id,
        chat_type,
        chat_title,
        user,
        text,
        thread_id=None,
        has_attachment=False,
        attachment_type=None,
        file_id=None,
        file_name=None,
        local_path=None,
        mime_type=None,
        file_size=None,
        timestamp=None
):
    """Log a message, including attachment flags and attachment type."""
    att_flag = 1 if has_attachment else 0
    
    with sqlite3.connect("messages.db") as conn:
        conn.row_factory = sqlite3.Row # prevent numerical index positions, so use dicts instead
        cursor = conn.cursor()
        if timestamp:
            cursor.execute(
                """
                INSERT INTO messages (chat_id, chat_type, thread_id, chat_title, user, text, has_attachment, attachment_type, file_id, file_name, local_path, mime_type, file_size, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (chat_id, chat_type, thread_id, chat_title, user, text, att_flag, attachment_type, file_id, file_name, local_path, mime_type, file_size, timestamp)
            )
        else:
            cursor.execute(
                """
                INSERT INTO messages (chat_id, chat_type, chat_title, user, text, has_attachment, attachment_type, file_id, file_name, local_path, mime_type, file_size, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (chat_id, chat_type, thread_id, chat_title, user, text, att_flag, attachment_type, file_id, file_name, local_path, mime_type, file_size, timestamp)
            )
        

def get_messages(chat_id: int, thread_id:int=None, since:str=None, hours:float=None):
    """Retrieve messages for a specific chat_id, optionally since a certain timestamp."""

    with sqlite3.connect("messages.db") as conn:
        conn.row_factory = sqlite3.Row # prevent numerical index positions, so use dicts instead
        cursor = conn.cursor()

        params = [chat_id]
        if thread_id is None or thread_id == 1:
            thread_clause = "AND (thread_id IS NULL OR thread_id = 1)"
        else:
            thread_clause = "AND thread_id = ?"
            params.append(int(thread_id))
            
        if since is not None:
            latest_dt = datetime.fromisoformat(since) # has T and is a datetime object
            prev_latest_dt = latest_dt
            latest_dt = latest_dt.isoformat(timespec="seconds") # becomes string
            latest_dt = latest_dt.replace("T", " ") # removes T
            thread_clause += " AND timestamp <= ?"
            params.append(latest_dt)
            
        if hours is not None:
            cutoff_dt = prev_latest_dt - timedelta(hours=hours) # has T and is a datetime object
            cutoff_dt = cutoff_dt.isoformat(timespec="seconds") # becomes string
            cutoff_dt = cutoff_dt.replace("T", " ") # removes T
            thread_clause += " AND timestamp >= ?"
            params.append(cutoff_dt)

        query = f"SELECT * FROM messages WHERE chat_id = ? {thread_clause} AND text IS NOT NULL AND text != '' ORDER BY id ASC"

        cursor.execute(query, params)
        return cursor.fetchall()

def clear_messages(chat_id, thread_id=None):
    """Clear all messages for a specific chat_id."""
    with sqlite3.connect("messages.db") as conn:
        conn.row_factory = sqlite3.Row # prevent numerical index positions, so use dicts instead
        cursor = conn.cursor()
        if thread_id is not None:
            cursor.execute("DELETE FROM messages WHERE chat_id = ? AND thread_id = ?", (chat_id, thread_id))
        else:
            cursor.execute("DELETE FROM messages WHERE chat_id = ? AND thread_id IS NULL", (chat_id,))

def count_messages(chat_id, thread_id=None, since:str=None, hours:float=None):
    """Count the number of messages for a specific chat_id, optionally since a certain timestamp til a certain hour."""

    with sqlite3.connect("messages.db") as conn:
        conn.row_factory = sqlite3.Row # prevent numerical index positions, so use dicts instead
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM messages WHERE chat_id = ? AND text IS NOT NULL AND text != ''"
        params = [chat_id]

        # Match both None and 1 for General topic, or exact ID for topics
        if thread_id is None or thread_id == 1:
            query += " AND (thread_id IS NULL OR thread_id = 1)"
        else:
            query += " AND thread_id = ?"
            params.append(thread_id)
        
        if since is not None:
            latest_dt = datetime.fromisoformat(since) # has T and is a datetime object
            prev_latest_dt = latest_dt
            latest_dt = latest_dt.isoformat(timespec="seconds") # becomes string
            latest_dt = latest_dt.replace("T", " ") # removes T
            query += " AND timestamp <= ?"
            params.append(latest_dt)
            
        if hours is not None:
            cutoff_dt = prev_latest_dt - timedelta(hours=hours) # has T and is a datetime object
            cutoff_dt = cutoff_dt.isoformat(timespec="seconds") # becomes string
            cutoff_dt = cutoff_dt.replace("T", " ") # removes T
            query += " AND timestamp >= ?"
            params.append(cutoff_dt)

        cursor.execute(query, params)
        return cursor.fetchone()[0]

def get_latest_message(chat_id: int, thread_id: int=None) -> str:
    """
    Retrieves the most recent message record from the database.
    Returns timestamp or None if the database is empty.
    """
    with sqlite3.connect("messages.db") as conn:
        conn.row_factory = sqlite3.Row # prevent numerical index positions, so use dicts instead
        cursor = conn.cursor()

        # Build clean parameter list
        params = [chat_id]
        
        # General topic (NULL or 1) vs Specific Thread Topic
        if thread_id is None or thread_id == 1:
            thread_clause = "AND (thread_id IS NULL OR thread_id = 1)"
        else:
            thread_clause = "AND thread_id = ?"
            params.append(int(thread_id))

        query = f"SELECT timestamp FROM messages WHERE chat_id = ? {thread_clause} ORDER BY id DESC LIMIT 1"

        cursor.execute(query, params)
        row = cursor.fetchone()
        
        return row[0] if row else None

