from telethon import TelegramClient
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
BOT_USERNAME = "solana_trojanbot"

# Create a Telegram client
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def list_chats():
    # Connect to Telegram
    await client.start()
    print("Connected to Telegram!")
    print("Fetching chats...")

    # Iterate through all dialogs and print chat names with IDs
    async for dialog in client.iter_dialogs():
        print(f"{dialog.name} has ID {dialog.id}")

async def main():
    await list_chats()

# Start the client and run the main function
with client:
    client.loop.run_until_complete(main())
