from collections import defaultdict
from app.memory.database import get_connection

conversation_history = defaultdict(list)

MAX_HISTORY = 4


def add_message(user_id, role, content):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations
        (
            user_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            role,
            content
        )
    )

    conn.commit()

    conn.close()


def get_history(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM conversations
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, MAX_HISTORY)
    )

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in rows
    ]

def clear_history(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM conversations
        WHERE user_id = ?
        """,
        (user_id,)
    )

    conn.commit()

    conn.close()