from app.core.openai_client import (
    create_response
)


class WebSearchTool:

    @staticmethod
    def search(
        query: str
    ):

        query = query[:300]
        
        response = create_response(

            model="gpt-5.4-mini",

            tools=[
                {
                    "type": "web_search"
                }
            ],

            input=query
        )

        return response.output_text