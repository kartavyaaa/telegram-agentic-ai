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

import logging

logger = logging.getLogger(__name__)


class AutonomousWorkflowService:

    MAX_ITERATIONS = 3
    MAX_RESULTS = 20

    @staticmethod
    async def run(
        user_question: str
    ):

        logger.info(
            "AUTONOMOUS WORKFLOW STARTED"
        )

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

            if len(all_results) > (AutonomousWorkflowService.MAX_RESULTS):
                
                break

            decision = (
                await ObserverService
                .evaluate_results(
                    user_question,
                    all_results
                )
            )

            logger.info(
                f"Iteration {iteration + 1}: {decision}"
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