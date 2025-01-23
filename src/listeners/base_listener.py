from telethon import TelegramClient

class BaseListener:
    def __init__(self, client: TelegramClient):
        """
        Initialize the BaseListener with a Telegram client.
        """
        self.client = client

    async def register_listener(self):
        """
        Subclasses must implement this method to register their specific listeners.
        """
        raise NotImplementedError("Subclasses must implement this method.")
