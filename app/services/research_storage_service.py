from app.memory.database import (
    get_connection
)


class ResearchStorageService:

    @staticmethod
    def save_result(
        task_id: int,
        query: str,
        result: str
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO research_results
            (
                task_id,
                query,
                result
            )
            VALUES (?, ?, ?)
            """,
            (
                task_id,
                query,
                result
            )
        )

        conn.commit()
        conn.close()


    @staticmethod
    def get_recent_results(
        limit: int = 20
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                query,
                result,
                created_at
            FROM research_results
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        conn.close()

        return rows