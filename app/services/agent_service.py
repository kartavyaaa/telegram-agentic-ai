from app.services.ai_service import AIService
from app.tools.tool_registry import TOOLS


class AgentService:

    @staticmethod
    async def process_message(
        user_message: str,
        history: list
    ):

        selected_tool = (await AIService.classify_tool(user_message)
        )

        print(f"Selected tool: {selected_tool}")
        
        if selected_tool != "none":

            return await AgentService.execute_tool(
                selected_tool,
                user_message
            )

        return await AIService.generate_response(
            user_message,
            history
        )
    
    @staticmethod
    async def execute_tool(
        tool_name: str,
        user_message: str
    ):

        if tool_name == "calculator":

            expression = (
                await AIService
                .extract_calculation_expression(
                user_message
            )
        )

            return TOOLS[
                tool_name
                ].calculate(
                expression
            )

        elif tool_name == "web_search":

            query = (
                await AIService
                .extract_search_query(
                user_message
            )
        )

            return TOOLS[
            tool_name
            ].search(
            query
            )
        
        elif tool_name == "rag_search":

            from app.services.rag_service import (
            RAGService
            )

            return await RAGService.answer_question(
                user_message
            )
        
        elif tool_name == "autonomous_workflow":

            from app.services.autonomous_workflow_service import (
                AutonomousWorkflowService
            )

            return await (
                AutonomousWorkflowService
                .run(
                    user_message
                )
            )

        return None