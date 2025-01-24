from telethon import TelegramClient
from dotenv import load_dotenv
import os

class TelegramClientSingleton:
    _instance = None  # Singleton instance

    @classmethod
    async def get_instance(cls):
        """
        Retrieve the singleton TelegramClient instance.
        If it does not exist, initialize and start it.
        """
        if cls._instance is None:
            load_dotenv()

            # Load environment variables
            TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
            TELEGRAM_API_ID = os.getenv("API_ID")
            TELEGRAM_API_HASH = os.getenv("API_HASH")
            SESSION_NAME = os.getenv("SESSION_NAME")

            # Ensure all required environment variables are set
            if not all([TELEGRAM_PHONE, TELEGRAM_API_ID, TELEGRAM_API_HASH, SESSION_NAME]):
                raise EnvironmentError("Missing one or more required environment variables. Check your .env file.")

            # Initialize and start the Telegram client
            client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
            await client.start(phone=TELEGRAM_PHONE)
            cls._instance = client

        return cls._instance
