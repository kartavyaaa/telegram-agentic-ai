from telegram import Update
from telegram.ext import ContextTypes

from openai import AsyncOpenAI

from app.core.config import settings

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Agent online."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = """
Available commands:

/start - Start the bot
/help - Show available commands
"""

    await update.message.reply_text(help_text)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    client = AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY
    )

    response = await client.chat.completions.create(

        model="gpt-5.4-mini",

        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    ai_reply = response.choices[0].message.content

    await update.message.reply_text(ai_reply)