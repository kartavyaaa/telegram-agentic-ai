import asyncio
import json

from app.tools.tool_registry import TOOLS


class WorkflowService:

    @staticmethod
    async def execute_plan(
        plan_json: str
    ):

        plan = json.loads(
            plan_json
        )

        tasks = []

        for step in plan:

            action = step["action"]

            if action == "web_search":

                tasks.append(
                    asyncio.to_thread(
                        TOOLS[
                            "web_search"
                        ].search,
                        step["input"]
                    )
                )

        search_results = (
            await asyncio.gather(
                *tasks
            )
        )

        results = []

        for result in search_results:

            results.append(
                {
                    "action": "web_search",
                    "result": result
                }
            )

        return results