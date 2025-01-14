from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

RICKBOT_ID = int(os.getenv("RICKBOT_ID"))
VISI_CHAT_ID = int(os.getenv("VISI_CHAT_ID"))
VISI_CHANNEL_ID = int(os.getenv("VISI_CHANNEL_ID"))
# TRENCHES_CALLS_SENDER_ID_IN_TRENCHES_CHAT = int(os.getenv("TRENCHES_CALLS_SENDER_ID_IN_TRENCHES_CHAT"))
# VISHNU_SENDER_ID = int(os.getenv("VISHNU_SENDER_ID"))
# SIDDHARTH_SENDER_ID = int(os.getenv("SIDDHARTH_SENDER_ID"))

# Telegram client setup
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

# List of chat IDs to monitor
chat_ids = [VISI_CHANNEL_ID, VISI_CHAT_ID]

# Event handler for new messages
@client.on(events.NewMessage(chats=chat_ids))
async def new_message_handler(event):
    print("New Message Event:")
    print(event)  # Log the entire event object for debugging

# Event handler for edited messages
@client.on(events.MessageEdited(chats=chat_ids))
async def edited_message_handler(event):
    print("Edited Message Event:")
    print(event)  # Log the entire event object for debugging

async def main():
    print("Message Logger is running...")
    print("Listening for new and edited messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
