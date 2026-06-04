import sqlite3


def get_total_tokens():

    conn = sqlite3.connect(
        "memory.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            COALESCE(
                SUM(total_tokens),
                0
            )
        FROM usage_logs
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total