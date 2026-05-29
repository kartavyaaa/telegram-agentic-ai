import asyncio

from app.services.observer_service import (
    ObserverService
)

async def main():

    result = (
        await ObserverService
        .evaluate_results(
            user_question=
            "Compare XUV 3XO EV and Nexon EV",

            workflow_results=[
                {
                    "result":
                    "XUV 3XO EV exists."
                }
            ]
        )
    )

    print(result)

asyncio.run(main())