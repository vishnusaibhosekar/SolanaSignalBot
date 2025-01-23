import os
from dotenv import load_dotenv
from telethon import TelegramClient
from listeners.trojan_listener import TrojanListener
from utils.logger import Logger

# Load environment variables
load_dotenv()

# Initialize Telegram credentials
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = os.getenv("API_ID")
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
TROJAN_CHAT_ID = int(os.getenv("TROJAN_CHAT_ID"))  # Trojan chat ID

# Ensure all environment variables are set
if not all([TELEGRAM_PHONE, TELEGRAM_API_ID, TELEGRAM_API_HASH, SESSION_NAME, TROJAN_CHAT_ID]):
    raise EnvironmentError("Missing one or more required environment variables. Check your .env file.")

# Initialize the logger
logger = Logger()

# Setup Telegram client
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

# Initialize the TrojanListener
async def main():
    print(f"Initializing TrojanListener for TROJAN_CHAT_ID: {TROJAN_CHAT_ID}")
    trojan_listener = TrojanListener(client, TROJAN_CHAT_ID)

    # Register the listener
    await trojan_listener.register_listener()

    print("TrojanListener is now active. Listening for messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    print("Starting temp_main.py")
    with client:
        client.loop.run_until_complete(main())
