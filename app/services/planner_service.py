import json

from app.core.openai_client import (
    create_chat_completion
)


class PlannerService:

    MAX_PLAN_STEPS = 5

    @staticmethod
    async def create_plan(
        user_message: str
    ):

        response = create_chat_completion(

            model="gpt-5.4-mini",

            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    You are an AI planner.

                    Available actions:

                    web_search
                    rag_search
                    calculator

                    Return a JSON list.

                    Example:

                    [
                        {
                            "action": "web_search",
                            "input": "Tesla Model Y specs"
                        },
                        {
                            "action": "web_search",
                            "input": "Hyundai Ioniq 5 specs"
                        }
                    ]

                    For questions involving:

                    - technology
                    - products
                    - phones
                    - cars
                    - software
                    - news
                    - current events

                    always search for the latest available
                    information.

                    Include words such as:

                    latest
                    current
                    2026

                    when appropriate.

                    Return ONLY JSON.
                    """
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        plan_json = (
            response
            .choices[0]
            .message.content
            .strip()
        )

        try:

            parsed_plan = json.loads(
                plan_json
            )

            if not isinstance(
                parsed_plan,
                list
            ):
                raise ValueError(
                    "Plan must be a list"
                )

            parsed_plan = parsed_plan[
                :PlannerService.MAX_PLAN_STEPS
            ]

            return json.dumps(
                parsed_plan
            )

        except Exception:

            # Safe fallback
            return json.dumps(
                [
                    {
                        "action": "web_search",
                        "input": user_message
                    }
                ]
            )