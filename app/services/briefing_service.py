from app.services.research_storage_service import (
    ResearchStorageService
)

from app.services.ai_service import (
    AIService
)


class BriefingService:

    @staticmethod
    async def generate():

        results = (
            ResearchStorageService
            .get_recent_results()
        )

        if not results:

            return (
                "No research results found."
            )

        combined_results = ""

        for (
            query,
            result,
            created_at
        ) in results:

            combined_results += (
                f"\n\nTopic: {query}\n"
                f"{result}\n"
            )

        prompt = f"""
Create a concise executive briefing.

Research Results:
{combined_results}

Format:

📰 Daily Briefing

🔥 Top Developments
...

📈 Trends
...

⚠ Risks
...

💡 Opportunities
...

🎯 Key Takeaways
...
"""

        return await AIService.generate_response(
            prompt,
            []
        )