from dotenv import load_dotenv

import os


load_dotenv(
    override=True
)


class Settings:

    def __init__(self):

        self.TELEGRAM_BOT_TOKEN = (
            os.getenv(
                "TELEGRAM_BOT_TOKEN"
            )
        )

        self.OPENAI_API_KEY = (
            os.getenv(
                "OPENAI_API_KEY"
            )
        )

        self.validate()

    def validate(self):

        missing = []

        if not self.TELEGRAM_BOT_TOKEN:

            missing.append(
                "TELEGRAM_BOT_TOKEN"
            )

        if not self.OPENAI_API_KEY:

            missing.append(
                "OPENAI_API_KEY"
            )

        if missing:

            raise ValueError(
                "Missing environment variables: "
                + ", ".join(missing)
            )


settings = Settings()