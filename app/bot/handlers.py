from telegram import Update
from telegram.ext import ContextTypes
from openai import AsyncOpenAI
from app.core.config import settings
from app.memory.conversation_memory import (
    add_message,
    get_history,
    clear_history
)
from app.services.ai_service import AIService
from app.services.agent_service import AgentService
from app.services.rag_service import (
    RAGService
)
from app.scheduler.task_manager import (
    TaskManager
)   

from pathlib import Path
from app.rag.ingest import ingest_pdf

from app.utils.telegram_utils import (
    send_long_message
)

from app.services.stats_service import (
    StatsService
)
from app.services.briefing_service import (
    BriefingService
)

from app.services.briefing_preference_service import (
    BriefingPreferenceService
)

async def autobriefing_command(
    update,
    context
):

    if not context.args:

        await update.message.reply_text(
            "Usage:\n"
            "/autobriefing HH:MM"
        )

        return

    user_id = (
        update.effective_user.id
    )

    briefing_time = (
        context.args[0]
    )

    parts = briefing_time.split(":")

    if len(parts) == 2:

        hour = int(parts[0])

        minute = int(parts[1])

        briefing_time = (
            f"{hour:02d}:{minute:02d}"
        )

    BriefingPreferenceService.save(
        user_id,
        briefing_time
    )

    await update.message.reply_text(
        f"✅ Auto briefing enabled\n\n"
        f"Time: {briefing_time}"
    )

async def briefing_command(
    update,
    context
):

    briefing = await (
        BriefingService.generate()
    )

    await update.message.reply_text(
        briefing
    )

async def stats_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    stats = (
        StatsService
        .get_stats()
    )

    await update.message.reply_text(
        stats
    )

async def rag_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.args:

        await update.message.reply_text(
            "Usage: /rag <question>"
        )

        return

    question = " ".join(
        context.args
    )

    answer = (
        await RAGService
        .answer_question(
            question
        )
    )

    await update.message.reply_text(
        answer
    )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Agent online."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = """
Available commands:

/start - Start the bot
/help - Show available commands
/reset - Clear all stored conversation memory
/rag <question> - Search your knowledge base
/stats - View usage statistics
/research daily 08:00 AI news
/tasks - View scheduled tasks
/deletetask <id> - Delete task
/briefing - Generate daily briefing
/autobriefing HH:MM
"""

    await update.message.reply_text(help_text)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    clear_history(user_id)

    await update.message.reply_text("Conversation memory cleared.")


from app.core.request_timer import (
    RequestTimer
)

import logging

logger = logging.getLogger(__name__)

async def message_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    user_message = update.message.text
    
    timer = RequestTimer()

    history = get_history(user_id)

    ai_reply = await AgentService.process_message(
        user_message=user_message,
        history=history
    )

    logger.info(
        f"Request completed in "
        f"{timer.elapsed()}s"
    )

    add_message(
        user_id,
        "user",
        user_message
    )

    assistant_memory = ai_reply

    if len(ai_reply) > 1000:

        assistant_memory = (
            ai_reply[:1000]
            + "\n\n[TRUNCATED]"
        )

    add_message(
        user_id,
        "assistant",
        assistant_memory
    )
    
    try:

        await send_long_message(
            update,
            ai_reply
        )

    except Exception as e:

        logger.exception(
            f"Failed to send response: {e}"
        )

async def document_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    print("Document Handler Triggered")
    document = update.message.document
    print(document)

    if not document:
        return

    if not document.file_name.lower().endswith(
        ".pdf"
    ):

        await update.message.reply_text(
            "Only PDF files are supported."
        )

        return

    telegram_file = (
        await document.get_file()
    )

    save_path = (
        Path("data/documents")
        / document.file_name
    )

    await telegram_file.download_to_drive(
        custom_path=str(save_path)
    )

    await update.message.reply_text(
        "PDF received. Ingesting..."
    )

    ingest_pdf(
        str(save_path)
    )

    await update.message.reply_text(
        "Document added to knowledge base."
    )

async def research_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if len(context.args) < 3:

        await update.message.reply_text(
            "Usage:\n"
            "/research daily 08:00 AI news"
        )

        return

    schedule_type = context.args[0]

    schedule_value = context.args[1]

    parts = schedule_value.split(":")

    if len(parts) == 2:

        hour = int(parts[0])

        minute = int(parts[1])

        schedule_value = (
            f"{hour:02d}:{minute:02d}"
        )

    query = " ".join(
        context.args[2:]
    )

    user_id = (
        update.effective_user.id
    )

    TaskManager.create_task(
        user_id=user_id,
        query=query,
        schedule_type=schedule_type,
        schedule_value=schedule_value
    )

    await update.message.reply_text(
        f"✅ Research task created\n\n"
        f"Query: {query}\n"
        f"Schedule: {schedule_type} "
        f"{schedule_value}"
    )


async def tasks_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = (
        update.effective_user.id
    )

    tasks = (
        TaskManager.get_tasks(
            user_id
        )
    )

    if not tasks:

        await update.message.reply_text(
            "No scheduled tasks found."
        )

        return

    response = (
        "📋 Scheduled Tasks\n\n"
    )

    for (
        task_id,
        query,
        schedule_type,
        schedule_value
    ) in tasks:

        response += (
            f"{task_id}. {query}\n"
            f"   {schedule_type} "
            f"{schedule_value}\n\n"
        )

    await update.message.reply_text(
        response
    )


async def deletetask_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.args:

        await update.message.reply_text(
            "Usage:\n"
            "/deletetask <task_id>"
        )

        return

    task_id = int(
        context.args[0]
    )

    user_id = (
        update.effective_user.id
    )

    TaskManager.delete_task(
        task_id,
        user_id
    )

    await update.message.reply_text(
        "✅ Task deleted"
    )