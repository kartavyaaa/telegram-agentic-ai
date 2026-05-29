from app.services.ai_service import AIService

import asyncio


async def main():

    result = (
        await AIService
        .extract_document_name(
            user_message=
            "What does my resume say about Python?",

            available_sources=[
                "Kartavya_Raina_Resume"
            ]
        )
    )

    print(result)

asyncio.run(main())