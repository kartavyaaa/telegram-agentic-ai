from app.services.planner_service import (
    PlannerService
)

from app.services.workflow_service import (
    WorkflowService
)

from app.services.observer_service import (
    ObserverService
)

from app.services.replanner_service import (
    ReplannerService
)

from app.services.ai_service import (
    AIService
)


class AutonomousWorkflowService:

    MAX_ITERATIONS = 3

    @staticmethod
    async def run(
        user_question: str
    ):

        plan = (
            await PlannerService
            .create_plan(
                user_question
            )
        )

        all_results = []

        for iteration in range(
            AutonomousWorkflowService
            .MAX_ITERATIONS
        ):

            results = (
                await WorkflowService
                .execute_plan(
                    plan
                )
            )

            all_results.extend(
                results
            )

            decision = (
                await ObserverService
                .evaluate_results(
                    user_question,
                    all_results
                )
            )

            print(
                f"Iteration "
                f"{iteration + 1}: "
                f"{decision}"
            )

            if decision == "sufficient":

                break

            plan = (
                await ReplannerService
                .create_followup_plan(
                    user_question,
                    all_results
                )
            )

        return (
            await AIService
            .synthesize_results(
                user_question,
                all_results
            )
        )