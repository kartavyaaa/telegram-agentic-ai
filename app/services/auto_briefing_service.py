from datetime import datetime

from app.services.briefing_service import (
    BriefingService
)

from app.services.briefing_preference_service import (
    BriefingPreferenceService
)

from app.core import bot_context


class AutoBriefingService:

    @staticmethod
    async def run():

        current_time = (
            datetime.now()
            .strftime("%H:%M")
        )

        today = (
            datetime.now()
            .date()
            .isoformat()
        )

        preferences = (
            BriefingPreferenceService
            .get_all()
        )

        for (
            user_id,
            briefing_time,
            last_sent
        ) in preferences:

            if (
                briefing_time
                != current_time
            ):
                continue

            if last_sent == today:
                continue

            briefing = (
                await BriefingService.generate()
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