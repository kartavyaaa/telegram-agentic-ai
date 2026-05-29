from app.rag.retriever import retrieve_context
from app.services.ai_service import AIService


class RAGService:

    @staticmethod
    async def answer_question(
        question: str
    ):

        context = retrieve_context(
            question
        )

        print("\nQUESTION:")
        print(question)

        print("\nRETRIEVED CONTEXT:")
        print(context)

        answer = (
            await AIService
            .answer_from_context(
                question,
                context
            )
        )

        return answer