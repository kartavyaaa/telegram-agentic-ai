import asyncio
import time
from app.services.planner_service import (
    PlannerService
)

from app.services.workflow_service import (
    WorkflowService
)
from app.services.ai_service import (
    AIService
)

async def main():
    start =time.time()
    plan = (
        await PlannerService
        .create_plan(
            "Compare XUV 3XO EV and Nexon EV"
        )
    )

    print("\nPLAN:\n")
    print(plan)

    results = (
        await WorkflowService
        .execute_plan(
            plan
        )
    )

    

    final_answer = (
        await AIService
        .synthesize_results(
            user_question=
            "Compare XUV 3XO EV and Nexon EV",

            workflow_results=
            results
        )
    )

    print("\nFINAL ANSWER:\n")
    print(final_answer)

    print("\nRESULTS:\n")

    for result in results:

        print(
            result["result"]
        )

        print(
            "\n"
            + "=" * 80
            + "\n"
        )
    end=time.time()
    print(f"\nTotal Time: "
          f"{round(end-start,2)} seconds")
        
asyncio.run(main())