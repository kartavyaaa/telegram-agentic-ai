from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


class AIService:

    @staticmethod
    async def generate_response(user_message: str) -> str:

        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Kartavya's personal AI assistant."
                        "You are intelligent, concise, and practical."
                    )
                },

                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return response.choices[0].message.content