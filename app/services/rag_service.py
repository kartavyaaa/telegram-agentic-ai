from app.services.ai_service import AIService
from app.rag.retriever import (retrieve_from_source, retrieve_context,get_available_sources)
from app.services.ai_service import AIService

class RAGService:

    @staticmethod
    async def answer_question(
        question: str
    ):

        sources = get_available_sources()

        source = (
            await AIService.extract_document_name(
                question,
                sources
            )
        )

        if source != "none":

            context = retrieve_from_source(
                query=question,
                source=source
            )

        else:

            context = retrieve_context(
                question
            )

        return await AIService.answer_from_context(
            question,
            context
        )
    
    @staticmethod
    async def answer_question_from_source(
        question: str,
        source: str
    ):

        context = retrieve_from_source(
            query=question,
            source=source
        )
        
        answer = (
            await AIService.answer_from_context(
                question,
                context
            )
        )

        return answer