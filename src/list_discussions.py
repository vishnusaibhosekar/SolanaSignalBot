from telethon import TelegramClient, events
from telethon.tl.types import PeerUser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
RICKBOT_ID = int(os.getenv("RICKBOT_ID"))

client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

@client.on(events.NewMessage)
async def handle_new_message(event):
    # Check if the message is from the discussion group
    if event.is_group:
        message = event.message
        print(f"New message from in discussion: {message.text} (ID: {message.id})")

        # Check if the sender is RickBot
        if message.from_id and isinstance(message.from_id, PeerUser):
            user_id = message.from_id.user_id
            if user_id == RICKBOT_ID:
                print(f"Message from RickBot: {message.text} (from_id: {user_id})")

# Start listening for messages
print("Listening for new messages...")
client.run_until_disconnected()
