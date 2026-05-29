from app.rag.retriever import (
    retrieve_context
)

from app.services.ai_service import (
    AIService
)

import asyncio


async def main():

    question = (
        "What does the report say "
        "about YouTube traffic?"
    )

    context = retrieve_context(
        question
    )

    answer = (
        await AIService
        .answer_from_context(
            question,
            context
        )
    )

    print(answer)


asyncio.run(main())