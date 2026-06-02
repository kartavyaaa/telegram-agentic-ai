import sqlite3


DB_NAME = "memory.db"



def get_connection():

    return sqlite3.connect(DB_NAME)

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            operation TEXT,

            prompt_tokens INTEGER,

            completion_tokens INTEGER,

            total_tokens INTEGER
        )
    """)

    conn.commit()

    conn.close()
    