import logging
import sqlite3


logger = logging.getLogger(__name__)


def log_usage(
    operation: str,
    usage
):

    if not usage:
        return

    prompt_tokens = getattr(
        usage,
        "prompt_tokens",
        0
    )

    completion_tokens = getattr(
        usage,
        "completion_tokens",
        0
    )

    total_tokens = getattr(
        usage,
        "total_tokens",
        0
    )

    logger.info(
        f"{operation} | "
        f"prompt={prompt_tokens} | "
        f"completion={completion_tokens} | "
        f"total={total_tokens}"
    )

    conn = sqlite3.connect(
        "memory.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usage_logs (

            operation,
            prompt_tokens,
            completion_tokens,
            total_tokens

        )

        VALUES (?, ?, ?, ?)
        """,
        (
            operation,
            prompt_tokens,
            completion_tokens,
            total_tokens
        )
    )

    conn.commit()
    conn.close()