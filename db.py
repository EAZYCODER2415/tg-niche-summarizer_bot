"""
db.py — SQLite database layer for the Telegram Summary Bot.

Replaces the in-memory `message_buffer` dict with SQLite commands.
This is a Python library using the SQLite module, to process and store messages
in a SQLite database from Telegram handlers.

"""

import os
import sqlite3
from datetime import datetime, timedelta

import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL_POOLED") or os.getenv("DATABASE_URL")

def get_connection():
    """Returns a Neon PostgreSQL connection if DATABASE_URL is present, else SQLite."""
    if DATABASE_URL:
        # Neon PostgreSQL connection
        return psycopg.connect(DATABASE_URL, row_factory=dict_row)
    else:
        # Local SQLite fallback for offline development
        conn = sqlite3.connect("messages.db")
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Initialize the SQLite database and create the messages table if it doesn't exist."""

    id_type = "SERIAL PRIMARY KEY" if DATABASE_URL else "INTEGER PRIMARY KEY AUTOINCREMENT"

    with get_connection() as conn:

        cursor = conn.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS messages (
                id {id_type},
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
    
    with get_connection() as conn:
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

    with get_connection() as conn:
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

        query = f"SELECT * FROM messages WHERE chat_id = ? {thread_clause} AND text IS NOT NULL AND text != '' ORDER BY id DESC"
        if hours is not None:
           query += " LIMIT 50"

        cursor.execute(query, params)
        return cursor.fetchall()

def clear_messages(chat_id, thread_id=None):
    """Clear all messages for a specific chat_id."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if thread_id is not None:
            cursor.execute("DELETE FROM messages WHERE chat_id = ? AND thread_id = ?", (chat_id, thread_id))
        else:
            cursor.execute("DELETE FROM messages WHERE chat_id = ? AND thread_id IS NULL", (chat_id))

def count_messages(chat_id, thread_id=None, since:str=None, hours:float=None):
    """Count the number of messages for a specific chat_id, optionally since a certain timestamp til a certain hour."""

    with get_connection() as conn:
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

def get_latest_message(chat_id: int=None, thread_id: int=None) -> str:
    """
    Retrieves the most recent message record from the database.
    Returns timestamp or None if the database is empty.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        if chat_id:
            # Build clean parameter list
            params = [chat_id]

            # General topic (NULL or 1) vs Specific Thread Topic
            if thread_id is None or thread_id == 1:
                thread_clause = "AND (thread_id IS NULL OR thread_id = 1)"
            else:
                thread_clause = "AND thread_id = ?"
                params.append(int(thread_id))

        if chat_id:
            query = f"SELECT timestamp FROM messages WHERE chat_id = ? {thread_clause} ORDER BY id DESC LIMIT 1"
        else:
            query = f"SELECT timestamp FROM messages WHERE ORDER BY id DESC LIMIT 1"

        cursor.execute(query, params)
        row = cursor.fetchone()
        
        return row[0] if row else None

def delete_old_messages(db_path: str = "messages.db", hours: int = 72) -> int:
    """Deletes messages older than the specified number of hours."""
    with get_connection() as conn:

        # Retrieve timestamp of most recent message
        since_time = get_latest_message()
        if not since_time:
            return 0  # Database is empty
        
        latest_dt = datetime.fromisoformat(since_time) # has T and is a datetime object
        latest_dt = latest_dt.isoformat(timespec="seconds") # becomes string
        latest_dt = latest_dt.replace("T", " ") # removes T
        params = [latest_dt, timestamp]
        
        # Safely pass latest_dt as a parameter; 'timestamp' is the table column
        query = """
            DELETE FROM messages 
            WHERE (julianday(?) - julianday(timestamp)) * 24 >= ?
        """

        # Execute deletion
        cursor.execute(query, (latest_dt, float(hours)))
        conn.commit()
        return cursor.rowcount

