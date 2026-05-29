from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


class WebSearchTool:

    @staticmethod
    def search(query: str):

        response = client.responses.create(
            model="gpt-5.4-mini",
            tools=[
                {
                    "type": "web_search"
                }
            ],
            input=query
        )

        return response.output_text