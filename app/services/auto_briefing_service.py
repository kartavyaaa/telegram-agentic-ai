from datetime import datetime

from app.services.briefing_service import (
    BriefingService
)

from app.services.briefing_preference_service import (
    BriefingPreferenceService
)

from app.core import bot_context

import logging

logger = logging.getLogger(__name__)


class AutoBriefingService:

    @staticmethod
    async def run():

        logger.info(
            "Checking auto briefings"
        )

        current_time = (
            datetime.now()
            .strftime("%H:%M")
        )

        today = (
            datetime.now()
            .date()
            .isoformat()
        )

        logger.info(
            f"Current briefing time: {current_time}"
        )

        preferences = (
            BriefingPreferenceService
            .get_all()
        )

        logger.info(
            f"Found {len(preferences)} briefing preferences"
        )

        for (
            user_id,
            briefing_time,
            last_sent
        ) in preferences:

            logger.info(
                f"Checking user {user_id} | "
                f"time={briefing_time} | "
                f"last_sent={last_sent}"
            )

            if briefing_time != current_time:

                logger.info(
                    f"Skipping user {user_id} "
                    f"(time mismatch)"
                )

                continue

            if last_sent == today:

                logger.info(
                    f"Skipping user {user_id} "
                    f"(already sent today)"
                )

                continue

            logger.info(
                f"Generating briefing for "
                f"user {user_id}"
            )

            briefing = (
                await BriefingService.generate()
            )

            logger.info(
                f"Sending briefing to "
                f"user {user_id}"
            )

            await (
                bot_context.application.bot
                .send_message(
                    chat_id=user_id,
                    text=briefing
                )
            )

            BriefingPreferenceService.update_last_sent(
                user_id,
                today
            )

            logger.info(
                f"Updated last_sent for "
                f"user {user_id}"
            )