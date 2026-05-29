from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


class PlannerService:

    @staticmethod
    async def create_plan(
        user_message: str
    ):

        response = client.chat.completions.create(

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

                    Return ONLY JSON.
                    """
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return (
            response
            .choices[0]
            .message.content
        )