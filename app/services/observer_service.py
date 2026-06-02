from app.core.config import settings
from openai import OpenAI
from app.core.openai_client import (
    create_chat_completion
)


class ObserverService:

    @staticmethod
    async def evaluate_results(
        user_question: str,
        workflow_results: list
    ):

        context = "\n\n".join(
            [
                result["result"]
                for result in workflow_results
            ]
        )

        response = create_chat_completion(

            model="gpt-5.4-mini",

            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    Determine whether enough information
                    exists to answer the user's question.

                    Consider:

                    - completeness
                    - accuracy
                    - relevance
                    - freshness for topics involving:
                    technology,
                    products,
                    pricing,
                    news,
                    vehicles,
                    current events

                    If the information appears outdated
                    or may not reflect the latest facts,
                    return:

                    insufficient

                    Return ONLY:

                    sufficient

                    or

                    insufficient
                    """
                },
                {
                    "role": "user",
                    "content":
                    f"""
                    Question:

                    {user_question}

                    Information:

                    {context}
                    """
                }
            ]
        )

        return (
            response
            .choices[0]
            .message.content
            .strip()
            .lower()
        )