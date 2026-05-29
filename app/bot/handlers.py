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

    await update.message.reply_text(ai_reply)