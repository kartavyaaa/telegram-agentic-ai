# app/utils/telegram_utils.py

import asyncio
import logging


logger = logging.getLogger(__name__)


async def send_long_message(
    update,
    text,
    chunk_size=4000
):

    chunks = [

        text[i:i + chunk_size]

        for i in range(
            0,
            len(text),
            chunk_size
        )
    ]

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        sent = False

        for attempt in range(
            1,
            4
        ):

            try:

                await update.message.reply_text(
                    chunk
                )

                sent = True

                break

            except Exception as e:

                logger.warning(
                    f"Telegram send failed "
                    f"(chunk={index}, "
                    f"attempt={attempt}/3): "
                    f"{e}"
                )

                await asyncio.sleep(
                    attempt
                )

        if not sent:

            logger.error(
                f"Failed to send chunk "
                f"{index}"
            )