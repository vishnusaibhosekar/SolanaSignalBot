from telethon import TelegramClient
from dotenv import load_dotenv
import os

class TelegramClientSingleton:
    _instance = None  # Singleton instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._initialize_client()
        return cls._instance

    @staticmethod
    def _initialize_client():
        load_dotenv()

        # Load environment variables
        TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
        TELEGRAM_API_ID = os.getenv("API_ID")
        TELEGRAM_API_HASH = os.getenv("API_HASH")
        SESSION_NAME = os.getenv("SESSION_NAME")

        # Ensure all required environment variables are set
        if not all([TELEGRAM_PHONE, TELEGRAM_API_ID, TELEGRAM_API_HASH, SESSION_NAME]):
            raise EnvironmentError("Missing one or more required environment variables. Check your .env file.")

        # Initialize and return Telegram client
        return TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)
