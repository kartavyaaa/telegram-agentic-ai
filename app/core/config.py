from dotenv import load_dotenv
load_dotenv(override=True)
import os

load_dotenv()

class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY").strip()

settings = Settings()