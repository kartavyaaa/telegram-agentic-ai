import sqlite3


class StatsService:

    @staticmethod
    def get_stats():

        conn = sqlite3.connect(
            "memory.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(
                    SUM(total_tokens),
                    0
                )
            FROM usage_logs
            """
        )

        total_requests, total_tokens = (
            cursor.fetchone()
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM usage_logs
            WHERE operation =
            'chat_completion'
            """
        )

        chat_requests = (
            cursor.fetchone()[0]
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM usage_logs
            WHERE operation =
            'response_api'
            """
        )

        search_requests = (
            cursor.fetchone()[0]
        )

        conn.close()

        average_tokens = 0

        if total_requests:

            average_tokens = round(
                total_tokens
                / total_requests
            )

        return (
            f"📊 Bot Statistics\n\n"

            f"Total Requests: "
            f"{total_requests}\n"

            f"Total Tokens: "
            f"{total_tokens:,}\n\n"

            f"Chat Completions:\n"
            f"• Requests: "
            f"{chat_requests}\n\n"

            f"Response API Searches:\n"
            f"• Requests: "
            f"{search_requests}\n\n"

            f"Average Tokens Per Request:\n"
            f"• {average_tokens:,}"
        )