import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from app.bot.handlers import (
    reset_command,
    start_command,
    message_handler,
    help_command,
    rag_command,
    document_handler,
    stats_command
)

from app.core.config import settings

import sys
print(sys.executable)

from app.memory.database import initialize_database

from app.utils.error_handler import (
    global_error_handler
)

from app.core.logging_config import (
    setup_logging
)


import logging

def main():

    setup_logging()

    logger = logging.getLogger(__name__)

    initialize_database()

    app = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("rag", rag_command))
    app.add_handler(MessageHandler(filters.Document.PDF,document_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message_handler))
    app.add_error_handler(global_error_handler)
    app.add_handler(CommandHandler("stats",stats_command))


    logger.info(
    "Bot is running..."
)

    app.run_polling()


if __name__ == "__main__":
    main()