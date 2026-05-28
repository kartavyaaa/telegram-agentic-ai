from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from app.bot.handlers import (
    start_command,
    message_handler
)

from app.core.config import settings


def main():

    app = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()