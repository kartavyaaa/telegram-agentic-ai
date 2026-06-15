import asyncio
import logging

from datetime import datetime

from app.scheduler.task_manager import (
    TaskManager
)

from app.core import bot_context

from app.services.autonomous_workflow_service import (
    AutonomousWorkflowService
)

logger = logging.getLogger(__name__)


class ResearchRunner:

    @staticmethod
    async def run():

        logger.info(
            "Research runner started"
        )

        while True:

            try:

                tasks = (
                    TaskManager
                    .get_due_tasks()
                )

                current_time = (
                    datetime.now()
                    .strftime("%H:%M")
                )

                logger.info(
                    f"Current time: {current_time}"
                )

                logger.info(
                    f"Found {len(tasks)} tasks"
                )

                for task in tasks:

                    (
                        task_id,
                        user_id,
                        query,
                        schedule_type,
                        schedule_value,
                        last_run
                    ) = task

                    if last_run:

                        logger.info(
                            f"Task {task_id} already executed"
                        )

                        continue

                    logger.info(
                        f"Checking task "
                        f"{task_id}: "
                        f"{schedule_value}"
                    )

                    if (
                        schedule_type == "daily"
                        and schedule_value == current_time
                    ):

                        logger.info(
                            f"Running task "
                            f"{task_id}: {query}"
                        )

                        result = await AutonomousWorkflowService.run(
                            query
                        )

                        logger.info(
                            f"Research completed: {query}"
                        )

                        logger.info(
                            result[:500]
                        )

                        await bot_context.application.bot.send_message(
                            chat_id=user_id,
                            text=(
                                f"🔔 Scheduled Research\n\n"
                                f"Query: {query}\n\n"
                                f"{result}"
                            )
                        )

                        TaskManager.mark_task_run(
                            task_id,
                            datetime.now().isoformat()
                        )

                await asyncio.sleep(60)

            except Exception as e:

                logger.exception(
                    f"Research runner error: {e}"
                )

                await asyncio.sleep(60)