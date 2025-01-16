from telethon import TelegramClient, events
from dotenv import load_dotenv
import asyncio
import os
from collections import deque
from utils.message_parser import extract_token_data
from trade_execution import automate_solana_trojan_bot

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

BULLX_CHAT_ID = int(os.getenv("BULLX_CHAT_ID"))

# Telegram client setup
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

@client.on(events.NewMessage(chats=BULLX_CHAT_ID))
async def new_message_handler(event):
    """
    Handles new messages in the BullX Chat.
    """
    print(f"\nNew message in BullX Chat: {event.message.text}")

async def main():
    print("Listening for new calls...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())