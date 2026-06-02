import sqlite3


conn = sqlite3.connect(
    "memory.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT

        COUNT(*),
        SUM(total_tokens)

    FROM usage_logs
    """
)

result = cursor.fetchone()

print(
    f"Requests: {result[0]}"
)

print(
    f"Total Tokens: {result[1]}"
)

conn.close()