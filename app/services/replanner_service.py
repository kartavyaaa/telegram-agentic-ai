from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


class ReplannerService:

    @staticmethod
    async def create_followup_plan(
        user_question: str,
        workflow_results: list
    ):

        context = "\n\n".join(
            [
                result["result"]
                for result in workflow_results
            ]
        )

        response = client.chat.completions.create(

            model="gpt-5.4-mini",

            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    The existing research is
                    insufficient.

                    Create ONLY the next
                    missing research steps.

                    Available actions:

                    web_search
                    rag_search

                    Return ONLY JSON.

                    Example:

                    [
                      {
                        "action": "web_search",
                        "input": "real world range comparison"
                      }
                    ]
                    """
                },
                {
                    "role": "user",
                    "content":
                    f"""
                    Original Question:

                    {user_question}

                    Existing Information:

                    {context}
                    """
                }
            ]
        )

        return (
            response
            .choices[0]
            .message.content
        )