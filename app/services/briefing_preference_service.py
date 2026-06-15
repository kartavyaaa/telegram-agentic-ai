from app.memory.database import (
    get_connection
)


class BriefingPreferenceService:

    @staticmethod
    def save(
        user_id: int,
        briefing_time: str
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO
            briefing_preferences
            (
                user_id,
                briefing_time,
                last_sent
            )
            VALUES
            (
                ?,
                ?,
                NULL
            )
            """,
            (
                user_id,
                briefing_time
            )
        )

        conn.commit()
        conn.close()


    @staticmethod
    def get_all():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                user_id,
                briefing_time,
                last_sent
            FROM briefing_preferences
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows


    @staticmethod
    def update_last_sent(
        user_id: int,
        sent_date: str
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE briefing_preferences
            SET last_sent = ?
            WHERE user_id = ?
            """,
            (
                sent_date,
                user_id
            )
        )

        conn.commit()
        conn.close()