# app/utils/telegram_utils.py

async def send_long_message(
    update,
    text,
    chunk_size=4000
):

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        await update.message.reply_text(
            text[i:i + chunk_size]
        )