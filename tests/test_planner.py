from app.services.planner_service import (
    PlannerService
)

import asyncio


async def main():

    plan = (
        await PlannerService
        .create_plan(
            "Compare XUV 3XO EV and Nexon EV"
        )
    )

    print(plan)

asyncio.run(main())