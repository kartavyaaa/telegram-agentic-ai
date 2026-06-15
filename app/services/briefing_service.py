from app.services.research_storage_service import (
    ResearchStorageService
)


class BriefingService:

    @staticmethod
    def generate():

        results = (
            ResearchStorageService
            .get_recent_results()
        )

        if not results:

            return (
                "No research results found."
            )

        briefing = (
            "📰 Daily Briefing\n\n"
        )

        for (
            query,
            result,
            created_at
        ) in results:

            briefing += (
                f"📌 {query}\n\n"
                f"{result[:300]}\n\n"
                f"━━━━━━━━━━━━━━\n\n"
            )

        return briefing