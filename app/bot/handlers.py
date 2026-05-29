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

from pathlib import Path
from app.rag.ingest import ingest_pdf

from app.utils.telegram_utils import (
    send_long_message
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
"""

    await update.message.reply_text(help_text)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    clear_history(user_id)

    await update.message.reply_text("Conversation memory cleared.")

async def message_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    user_message = update.message.text

    history = get_history(user_id)

    ai_reply = await AgentService.process_message(
        user_message=user_message,
        history=history
    )

    add_message(
        user_id,
        "user",
        user_message
    )

    add_message(
        user_id,
        "assistant",
        ai_reply
    )
    
    await send_long_message(
        update,
        ai_reply
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