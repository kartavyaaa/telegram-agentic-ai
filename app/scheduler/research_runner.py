import asyncio
import logging

from datetime import datetime

from app.scheduler.task_manager import (
    TaskManager
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

                for task in tasks:

                    (
                        task_id,
                        user_id,
                        query,
                        schedule_type,
                        schedule_value,
                        last_run
                    ) = task

                    if (
                        schedule_type == "daily"
                        and schedule_value == current_time
                    ):

                        logger.info(
                            f"Running task "
                            f"{task_id}: {query}"
                        )

                        print(
                            f"TASK DUE -> "
                            f"{query}"
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