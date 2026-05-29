from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
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

        response = client.chat.completions.create(

            model="gpt-5.4-mini",

            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    Determine whether enough
                    information exists to answer
                    the user's question.

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