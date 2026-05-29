from multiprocessing import context
from urllib import response

from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


class AIService:

    @staticmethod
    async def generate_response(
        user_message: str,
        history: list
    ) -> str:

        messages = [
            {
                "role": "system",
                "content":
                (
                    "You are Kartavya's personal AI assistant. "
                    "You are intelligent, concise, and practical."
                )
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            temperature=0.3,
            messages=messages
        )

        return response.choices[0].message.content
    
    @staticmethod
    async def classify_tool(user_message: str) -> str:

        messages=[
            {
                "role": "system",
                "content":
                """
                You are a tool classifier.

                Available tools:

                calculator
                web_search
                rag_search

                Use calculator for:
                - arithmetic
                - mathematical expressions

                Use web_search for:
                - latest news
                - current events
                - recent developments
                - live information
                - up-to-date facts

                Use rag_search for:
                - questions about uploaded documents
                - questions about reports
                - questions about internal knowledge
                - questions that mention:
                report
                document
                pdf
                notes
                knowledge base

                Return ONLY one word:

                calculator
                web_search
                rag_search
                none
                """
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    
        response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=messages
        )

        return response.choices[0].message.content.strip().lower()
    
    @staticmethod
    async def extract_calculation_expression(user_message: str) -> str:

        messages=[
            {
                "role": "system",
                "content":
                """
                Extract the mathematical expression from
                the user's request.

                Return ONLY the expression.

                Examples:

                What is 57 * 83?
                ->
                57 * 83

                Calculate (15 + 5) * 3
                ->
                (15 + 5) * 3

                Multiply 120 by 8
                ->
                120 * 8
                """
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=messages
        )

        return response.choices[0].message.content.strip()

    @staticmethod
    async def extract_search_query(
    user_message: str
) -> str:

            return user_message
    
    @staticmethod
    async def answer_from_context(
        question: str,
        context_chunks: list
    ):

        context = "\n\n".join(
            context_chunks
        )

        response = client.chat.completions.create(
            
            model="gpt-5.4-mini",

            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    Use the provided context to answer the question.

                    Be concise and factual.
                    """
                    
                },
                {
                    "role": "user",
                    "content":
                    f"""
                    Context:

                    {context}

                    Question:

                    {question}
                 """
                }
            ]
        )

        return response.choices[
            0
        ].message.content
    
    @staticmethod
    async def extract_document_name(
        user_message: str,
        available_sources: list
    ) -> str:

        response = client.chat.completions.create(

            model="gpt-5.4-mini",

            messages=[
                {
                    "role": "system",
                    "content":
                    f"""
                    Choose the most relevant document.

                    Available documents:

                    {available_sources}

                    Return ONLY the document name.

                    If none match, return:

                    none
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
            .strip()
        )
    
    @staticmethod
    async def synthesize_results(
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
                    You are an expert analyst.

                    Review all gathered information.

                    Produce one final answer.

                    Compare, analyze, and recommend
                    when appropriate.
                    """
                },
                {
                    "role": "user",
                    "content":
                    f"""
                    Original Question:

                    {user_question}

                    Research Results:

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