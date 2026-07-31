"""
db.py — SQLite database layer for the Telegram Summary Bot.

Replaces the in-memory `message_buffer` dict with SQLite commands.
This is a Python library using the SQLite module, to process and store messages
in a SQLite database from Telegram handlers.

"""

import sqlite3

def init_db():
    """Initialize the SQLite database and create the messages table if it doesn't exist."""
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                chat_type TEXT NOT NULL,
                chat_title TEXT,
                user TEXT NOT NULL,
                text TEXT NOT NULL,
                has_attachment BOOLEAN DEFAULT 0,
                attachment_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

def log_message(chat_id, chat_type, chat_title, user, text, has_attachment=False, attachment_type=None, timestamp=None):
    """Log a message, including attachment flags and attachment type."""
    att_flag = 1 if has_attachment else 0
    
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        if timestamp:
            cursor.execute(
                """
                INSERT INTO messages (chat_id, chat_type, chat_title, user, text, has_attachment, attachment_type, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (chat_id, chat_type, chat_title, user, text, att_flag, attachment_type, timestamp)
            )
        else:
            cursor.execute(
                """
                INSERT INTO messages (chat_id, chat_type, chat_title, user, text, has_attachment, attachment_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (chat_id, chat_type, chat_title, user, text, att_flag, attachment_type)
            )
        

def get_messages(chat_id, since=None):
    """Retrieve messages for a specific chat_id, optionally since a certain timestamp."""
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        if since:
            cursor.execute(
                "SELECT user, text, timestamp FROM messages WHERE chat_id = ? AND timestamp >= ? ORDER BY timestamp ASC",
                (chat_id, since),
            )
        else:
            cursor.execute(
                "SELECT user, text, timestamp FROM messages WHERE chat_id = ? ORDER BY timestamp ASC",
                (chat_id,),
            )
        messages = cursor.fetchall()
        return messages

def mark_as_summarized(chat_id, up_to_id):
    """Mark messages as summarized up to a certain message ID for a specific chat_id."""
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM messages WHERE chat_id = ? AND id <= ?",
            (chat_id, up_to_id),
        )

def clear_messages(chat_id):
    """Clear all messages for a specific chat_id."""
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM messages WHERE chat_id = ?",
            (chat_id,),
        )

def count_messages(chat_id, since=None):
    """Count the number of messages for a specific chat_id, optionally since a certain timestamp."""
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        if since:
            cursor.execute(
                "SELECT COUNT(*) FROM messages WHERE chat_id = ? AND timestamp >= ?",
                (chat_id, since),
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM messages WHERE chat_id = ?",
                (chat_id,),
            )
        count = cursor.fetchone()[0]
        return count

def get_tagged_messages(chat_id, tag):
    """Retrieve messages for a specific chat_id that contain a specific tag."""
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user, text, timestamp FROM messages WHERE chat_id = ? AND text LIKE ? ORDER BY timestamp ASC",
            (chat_id, f"%{tag}%"),
        )
        messages = cursor.fetchall()
        
        return messages

