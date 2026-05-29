import asyncio

from app.services.autonomous_workflow_service import (
    AutonomousWorkflowService
)


async def main():

    answer = (
        await AutonomousWorkflowService
        .run(
            "Compare XUV 3XO EV and Nexon EV"
        )
    )

    print("\nFINAL ANSWER:\n")
    print(answer)


asyncio.run(main())