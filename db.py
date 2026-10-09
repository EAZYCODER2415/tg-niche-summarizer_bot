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
from psycopg_pool import ConnectionPool

DATABASE_URL = os.getenv("DATABASE_URL_POOLED") or os.getenv("DATABASE_URL")

pool = None
if DATABASE_URL:
    pool = ConnectionPool(
        conninfo=DATABASE_URL,
        min_size=1,
        max_size=10,
        kwargs={"row_factory": dict_row},
        open=True,
        check=ConnectionPool.check_connection,
        max_idle=300,
        max_lifetime=1800
    )

def get_connection():
    """Returns a connection from the Neon PostgreSQL pool if available, else SQLite."""
    if pool:
        return pool.connection()
    else:
        # Local SQLite fallback
        conn = sqlite3.connect("messages.db")
        conn.row_factory = sqlite3.Row
        return conn

def execute_query(cursor, query: str, params: tuple = ()):
    if DATABASE_URL:
        # Automatically translate SQLite '?' placeholders to PostgreSQL '%s'
        query = query.replace("?", "%s")
    cursor.execute(query, params)

# -------------------- MAIN DATABASE (handling messages) --------------------------

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
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_summarized BOOLEAN DEFAULT FALSE
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
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_summarized BOOLEAN DEFAULT FALSE
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
        timestamp=None,
        is_summarized=False
):
    """Log a message, including attachment flags and attachment type."""
    att_flag = bool(has_attachment)
    
    # 1. Define column list
    cols = ["chat_id", "chat_type", "thread_id", "chat_title", "user" if not DATABASE_URL else '"user"',
            "text", "has_attachment", "attachment_type", "file_id", "file_name", 
            "local_path", "mime_type", "file_size", "timestamp", "is_summarized"]
    
    # 2. Pick placeholder style dynamically
    placeholder = "%s" if DATABASE_URL else "?"
    placeholders = ", ".join([placeholder] * len(cols))
    columns_str = ", ".join(cols)
    
    query = f"INSERT INTO messages ({columns_str}) VALUES ({placeholders});"
    
    params = (
        chat_id, chat_type, thread_id, chat_title, user, text,
        att_flag, attachment_type, file_id, file_name,
        local_path, mime_type, file_size, timestamp, False
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
            if isinstance(since, str):
                latest_dt = datetime.fromisoformat(since)
            else:
                latest_dt = since

            thread_clause += f" AND timestamp <= {placeholder}"
            params.append(latest_dt)
            
        if hours is not None:
            cutoff_dt = latest_dt - timedelta(hours=hours) # has T and is a datetime object
            thread_clause += f" AND timestamp >= {placeholder}"
            params.append(cutoff_dt)

        thread_clause += f" AND (is_summarized IS NULL OR is_summarized = FALSE)"

        query = f"SELECT * FROM messages WHERE chat_id = {placeholder} {thread_clause} AND text IS NOT NULL AND text != '' ORDER BY id ASC LIMIT 200"

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
        
        query = f"SELECT COUNT(*) AS total FROM messages WHERE chat_id = {placeholder} AND text IS NOT NULL AND text != ''"
        params = [chat_id]

        # Match both None and 1 for General topic, or exact ID for topics
        if thread_id is None or thread_id == 1:
            query += " AND (thread_id IS NULL OR thread_id = 1)"
        else:
            query += f" AND thread_id = {placeholder}"
            params.append(thread_id)
        
        if since is not None:
            if isinstance(since, str):
                latest_dt = datetime.fromisoformat(since)
            else:
                latest_dt = since
            
            query += f" AND timestamp <= {placeholder}"
            params.append(latest_dt)
            
        if hours is not None and latest_dt is not None:
            cutoff_dt = latest_dt - timedelta(hours=hours) # has T and is a datetime object
            query += f" AND timestamp >= {placeholder}"
            params.append(cutoff_dt)

        cursor.execute(query, params)
        # Inside count_messages() in db.py
        result = cursor.fetchone()

        # Check if result exists and access by key
        return result["total"] if result else 0

def get_latest_message(chat_id: int=None, thread_id: int=None) -> datetime | None:
    """
    Retrieves the most recent message record from the database.
    Returns timestamp or None if the database is empty.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        placeholder = "%s" if DATABASE_URL else "?"
        params = []

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
            query = f"SELECT timestamp FROM messages ORDER BY id DESC LIMIT 1"

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

def mark_as_summarized(message_ids: list[int]) -> int:
    """
    Marks messages as summarized given a list of message IDs.
    Returns the count of updated rows.
    """
    if not message_ids:
        return 0

    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Generates '%s, %s, ...' for Postgres or '?, ?, ...' for SQLite
        placeholder = "%s" if DATABASE_URL else "?"
        placeholders = ", ".join([placeholder] * len(message_ids))
        
        query = f"UPDATE messages SET is_summarized = TRUE WHERE id IN ({placeholders})"
        cursor.execute(query, message_ids)
        
        updated_count = cursor.rowcount
        conn.commit()
        
        return updated_count

# -------------------------- CHAT METADATA (handles chat settings and activity-threshold summaries) -------------------------------

def get_or_create_chat_metadata(chat_id: int, thread_id: int | None = None) -> dict:
    """
    Ensures the chat is initialized in chat_metadata, then fetches its current settings.
    """
    insert_query = """
        INSERT INTO chat_metadata (chat_id, thread_id, summary_thread_id, is_enabled, message_count, updated_at)
        VALUES (%s, %s, NULL, TRUE, 0, CURRENT_TIMESTAMP)
        ON CONFLICT (chat_id) DO NOTHING;
    """
    select_query = """
        SELECT summary_thread_id, is_enabled, message_count 
        FROM chat_metadata 
        WHERE chat_id = %s AND thread_id = %s;
    """
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Initialize if not present
            cur.execute(insert_query, (chat_id, thread_id))
            # Fetch guaranteed record
            cur.execute(select_query, (chat_id, thread_id))
            return cur.fetchone()

def update_chat_settings(chat_id: int, summary_thread_id: int | None = None, is_enabled: bool = True) -> None:
    """Updates or initializes topic routing and summary enablement settings."""
    query = """
        INSERT INTO chat_metadata (chat_id, summary_thread_id, is_enabled, message_count)
        VALUES (%s, %s, %s, 0)
        ON CONFLICT (chat_id) 
        DO UPDATE SET 
            summary_thread_id = EXCLUDED.summary_thread_id,
            is_enabled = EXCLUDED.is_enabled,
            updated_at = CURRENT_TIMESTAMP;
    """
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (chat_id, summary_thread_id, is_enabled))


def get_chat_settings(chat_id: int) -> dict:
    """Retrieves chat configuration (destination topic, status, and message count)."""
    query = """
        SELECT summary_thread_id, is_enabled, message_count 
        FROM chat_metadata 
        WHERE chat_id = %s;
    """
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, (chat_id,))
            row = cur.fetchone()
            if row:
                return row
            # Default settings for new chats
            return {"summary_thread_id": None, "is_enabled": True, "message_count": 0}


def increment_message_count(chat_id: int) -> int:
    """
    Increments and returns the current message count for triggering activity summaries.
    Atomic operation prevents race conditions across concurrent messages.
    """
    query = """
        INSERT INTO chat_metadata (chat_id, summary_thread_id, is_enabled, message_count)
        VALUES (%s, NULL, TRUE, 1)
        ON CONFLICT (chat_id) 
        DO UPDATE SET 
            message_count = chat_metadata.message_count + 1,
            updated_at = CURRENT_TIMESTAMP
        RETURNING message_count;
    """
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (chat_id,))
            new_count = cur.fetchone()[0]
            return new_count


def reset_message_count(chat_id: int, thread_id: int | None = None) -> None:
    """Resets the message counter back to zero after generating a summary."""
    query = """
        UPDATE chat_metadata 
        SET message_count = 0, updated_at = CURRENT_TIMESTAMP 
        WHERE chat_id = %s AND thread_id = %s;
    """
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (chat_id, thread_id))