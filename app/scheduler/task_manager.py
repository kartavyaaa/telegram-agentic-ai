from app.memory.database import (
    get_connection
)


class TaskManager:

    @staticmethod
    def create_task(
        user_id: int,
        query: str,
        schedule_type: str,
        schedule_value: str
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO scheduled_tasks
            (
                user_id,
                query,
                schedule_type,
                schedule_value
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                query,
                schedule_type,
                schedule_value
            )
        )

        conn.commit()
        conn.close()


    @staticmethod
    def get_tasks(
        user_id: int
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                query,
                schedule_type,
                schedule_value
            FROM scheduled_tasks
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        conn.close()

        return rows


    @staticmethod
    def delete_task(
        task_id: int,
        user_id: int
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM scheduled_tasks
            WHERE id = ?
            AND user_id = ?
            """,
            (
                task_id,
                user_id
            )
        )

        conn.commit()
        conn.close()


    @staticmethod
    def get_due_tasks():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                query,
                schedule_type,
                schedule_value,
                last_run
            FROM scheduled_tasks
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows


    @staticmethod
    def mark_task_run(
        task_id: int,
        timestamp: str
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE scheduled_tasks
            SET last_run = ?
            WHERE id = ?
            """,
            (
                timestamp,
                task_id
            )
        )

        conn.commit()
        conn.close()