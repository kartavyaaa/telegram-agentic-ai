from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Agent online."
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = f"You said: {user_message}"

    await update.message.reply_text(response)