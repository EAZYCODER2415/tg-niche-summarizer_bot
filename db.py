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

def execute_query(cursor, query: str, params: tuple = ()):
    if DATABASE_URL:
        # Automatically translate SQLite '?' placeholders to PostgreSQL '%s'
        query = query.replace("?", "%s")
    cursor.execute(query, params)

def init_db():
    """Initialize the SQLite database and create the messages table if it doesn't exist."""

    id_type = "SERIAL PRIMARY KEY" if DATABASE_URL else "INTEGER PRIMARY KEY AUTOINCREMENT"

    with get_connection() as conn:
        cursor = conn.cursor()
        if DATABASE_URL:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS messages (
                    id {id_type},
                    chat_id BIGINT NOT NULL,
                    chat_type TEXT NOT NULL,
                    thread_id BIGINT,
                    chat_title TEXT,
                    "user" TEXT NOT NULL,
                    text TEXT NOT NULL,
                    has_attachment BOOLEAN DEFAULT FALSE,
                    attachment_type TEXT,
                    file_id TEXT,
                    file_name TEXT,
                    local_path TEXT,
                    mime_type TEXT,
                    file_size BIGINT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        else:
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
                    has_attachment BOOLEAN DEFAULT FALSE,
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
        conn.commit()

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
    att_flag = bool(has_attachment)
    
    # 1. Define column list
    cols = ["chat_id", "chat_type", "thread_id", "chat_title", "user" if not DATABASE_URL else '"user"',
            "text", "has_attachment", "attachment_type", "file_id", "file_name", 
            "local_path", "mime_type", "file_size", "timestamp"]
    
    # 2. Pick placeholder style dynamically
    placeholder = "%s" if DATABASE_URL else "?"
    placeholders = ", ".join([placeholder] * len(cols))
    columns_str = ", ".join(cols)
    
    query = f"INSERT INTO messages ({columns_str}) VALUES ({placeholders});"
    
    params = (
        chat_id, chat_type, thread_id, chat_title, user, text,
        att_flag, attachment_type, file_id, file_name,
        local_path, mime_type, file_size, timestamp
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        

def get_messages(chat_id: int, thread_id:int=None, since:str=None, hours:float=None):
    """Retrieve messages for a specific chat_id, optionally since a certain timestamp."""

    with get_connection() as conn:
        cursor = conn.cursor()
        placeholder = "%s" if DATABASE_URL else "?"

        params = [chat_id]
        if thread_id is None or thread_id == 1:
            thread_clause = "AND (thread_id IS NULL OR thread_id = 1)"
        else:
            thread_clause = f"AND thread_id = {placeholder}"
            params.append(int(thread_id))
            
        if since is not None:
            latest_dt = datetime.fromisoformat(since) # has T and is a datetime object
            prev_latest_dt = latest_dt
            latest_dt = latest_dt.isoformat(timespec="seconds") # becomes string
            latest_dt = latest_dt.replace("T", " ") # removes T
            thread_clause += f" AND timestamp <= {placeholder}"
            params.append(latest_dt)
            
        if hours is not None:
            cutoff_dt = prev_latest_dt - timedelta(hours=hours) # has T and is a datetime object
            cutoff_dt = cutoff_dt.isoformat(timespec="seconds") # becomes string
            cutoff_dt = cutoff_dt.replace("T", " ") # removes T
            thread_clause += f" AND timestamp >= {placeholder}"
            params.append(cutoff_dt)

        query = f"SELECT * FROM messages WHERE chat_id = {placeholder} {thread_clause} AND text IS NOT NULL AND text != '' ORDER BY id DESC"
        if hours is not None:
           query += " LIMIT 50"

        cursor.execute(query, params)
        return cursor.fetchall()

def clear_messages(chat_id, thread_id=None):
    """Clear all messages for a specific chat_id."""
    with get_connection() as conn:
        cursor = conn.cursor()
        placeholder = "%s" if DATABASE_URL else "?"
        if thread_id is not None:
            query = f"DELETE FROM messages WHERE chat_id = {placeholder} AND thread_id = {placeholder}"
            cursor.execute(query, (chat_id, thread_id))
        else:
            query = f"DELETE FROM messages WHERE chat_id = {placeholder} AND thread_id IS NULL"
            cursor.execute(query, (chat_id,))

def count_messages(chat_id, thread_id=None, since:str=None, hours:float=None):
    """Count the number of messages for a specific chat_id, optionally since a certain timestamp til a certain hour."""

    with get_connection() as conn:
        cursor = conn.cursor()
        placeholder = "%s" if DATABASE_URL else "?"
        
        query = f"SELECT COUNT(*) FROM messages WHERE chat_id = {placeholder} AND text IS NOT NULL AND text != ''"
        params = [chat_id]

        # Match both None and 1 for General topic, or exact ID for topics
        if thread_id is None or thread_id == 1:
            query += " AND (thread_id IS NULL OR thread_id = 1)"
        else:
            query += f" AND thread_id = {placeholder}"
            params.append(thread_id)
        
        if since is not None:
            latest_dt = datetime.fromisoformat(since) # has T and is a datetime object
            prev_latest_dt = latest_dt
            latest_dt = latest_dt.isoformat(timespec="seconds") # becomes string
            latest_dt = latest_dt.replace("T", " ") # removes T
            query += f" AND timestamp <= {placeholder}"
            params.append(latest_dt)
            
        if hours is not None:
            cutoff_dt = prev_latest_dt - timedelta(hours=hours) # has T and is a datetime object
            cutoff_dt = cutoff_dt.isoformat(timespec="seconds") # becomes string
            cutoff_dt = cutoff_dt.replace("T", " ") # removes T
            query += f" AND timestamp >= {placeholder}"
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
        placeholder = "%s" if DATABASE_URL else "?"

        if chat_id:
            # Build clean parameter list
            params = [chat_id]

            # General topic (NULL or 1) vs Specific Thread Topic
            if thread_id is None or thread_id == 1:
                thread_clause = "AND (thread_id IS NULL OR thread_id = 1)"
            else:
                thread_clause = f"AND thread_id = {placeholder}"
                params.append(int(thread_id))

        if chat_id:
            query = f"SELECT timestamp FROM messages WHERE chat_id = {placeholder} {thread_clause} ORDER BY id DESC LIMIT 1"
        else:
            query = f"SELECT timestamp FROM messages WHERE ORDER BY id DESC LIMIT 1"

        cursor.execute(query, params)
        row = cursor.fetchone()
        
        if not row:
            return None
        return row["timestamp"] if DATABASE_URL else row[0]

def delete_old_messages(hours: int = 72) -> int:
    """Deletes messages older than the specified number of hours."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Retrieve timestamp of most recent message
        since_time = get_latest_message()
        if not since_time:
            return 0  # Database is empty
        
        latest_dt = datetime.fromisoformat(since_time) # has T and is a datetime object
        latest_dt = latest_dt.isoformat(timespec="seconds") # becomes string
        latest_dt = latest_dt.replace("T", " ") # removes T
        
        # Safely pass latest_dt as a parameter; 'timestamp' is the table column
        if DATABASE_URL:
            query = """
                DELETE FROM messages 
                WHERE timestamp < NOW() - (%s || ' hours')::INTERVAL
            """
            cursor.execute(query, (str(hours),))
        else:
            query = """
                DELETE FROM messages 
                WHERE (julianday('now') - julianday(timestamp)) * 24 >= ?
            """
            # Execute deletion
            cursor.execute(query, (float(hours),))

        deleted_count = cursor.rowcount
        conn.commit()
        return deleted_count

