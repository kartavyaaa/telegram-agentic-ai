import asyncio

from app.services.replanner_service import (
    ReplannerService
)


async def main():

    plan = (
        await ReplannerService
        .create_followup_plan(
            user_question=
            "Compare XUV 3XO EV and Nexon EV",

            workflow_results=[
                {
                    "result":
                    """
                    XUV 3XO EV:
                    Price 13.89 lakh
                    Battery 39.4 kWh
                    """
                }
            ]
        )
    )

    print(plan)


asyncio.run(main())