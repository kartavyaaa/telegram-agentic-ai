import logging

logger = logging.getLogger(__name__)


async def global_error_handler(
    update,
    context
):
    """
    Handles all uncaught exceptions.
    """

    logger.exception(
        "Unhandled exception occurred",
        exc_info=context.error
    )

    try:

        if (
            update
            and getattr(
                update,
                "effective_message",
                None
            )
        ):

            await (
                update.effective_message
                .reply_text(
                    "⚠️ Something went wrong while processing your request."
                )
            )

    except Exception:

        logger.exception(
            "Failed to send error message to user"
        )