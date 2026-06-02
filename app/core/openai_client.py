from openai import OpenAI

from app.core.config import settings
from app.core.usage_tracker import (
    log_usage
)

import logging
import time


logger = logging.getLogger(__name__)


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def create_chat_completion(
    **kwargs
):

    max_retries = 3

    for attempt in range(
        1,
        max_retries + 1
    ):

        try:

            response = (
                client
                .chat
                .completions
                .create(
                    **kwargs
                )
            )

            try:

                log_usage(
                    "chat_completion",
                    response.usage
                )

            except Exception as e:

                logger.warning(
                    f"Usage logging failed: {e}"
                )

            return response

        except Exception as e:

            logger.warning(
                f"OpenAI call failed "
                f"(attempt {attempt}/"
                f"{max_retries}): "
                f"{e}"
            )

            if attempt == max_retries:

                logger.exception(
                    "OpenAI call failed permanently"
                )

                raise

            time.sleep(
                2 * attempt
            )


def create_response(
    **kwargs
):

    max_retries = 3

    for attempt in range(
        1,
        max_retries + 1
    ):

        try:

            response = (
                client
                .responses
                .create(
                    **kwargs
                )
            )

            try:

                if hasattr(
                    response,
                    "usage"
                ):

                    log_usage(
                        "response_api",
                        response.usage
                    )

            except Exception as e:

                logger.warning(
                    f"Usage logging failed: {e}"
                )

            return response

        except Exception as e:

            logger.warning(
                f"OpenAI response call failed "
                f"(attempt {attempt}/"
                f"{max_retries}): "
                f"{e}"
            )

            if attempt == max_retries:

                logger.exception(
                    "OpenAI response call failed permanently"
                )

                raise

            time.sleep(
                2 * attempt
            )