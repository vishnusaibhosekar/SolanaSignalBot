from telethon import TelegramClient
from telethon.tl.types import MessageService
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

# Create a Telegram client
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def list_messages(chat_id: int, output_csv: str):
    # Connect to Telegram
    await client.start()
    print(f"Fetching messages for chat ID: {chat_id}...")

    # Open the CSV file for writing
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(["timestamp", "event_type", "message_id", "sender_id", "message_text"])

        # Iterate through all messages in the chat
        async for message in client.iter_messages(chat_id, reverse=True):
            timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else "N/A"
            event_type = "Service" if isinstance(message, MessageService) else "Message"
            message_id = message.id
            message_text = message.message or ""
            writer.writerow([timestamp, event_type, message_id, message.sender_id, message_text])

    print(f"Messages have been saved to {output_csv}.")

async def main():
    chat_id = int(input("Enter the chat ID: "))
    output_csv = "chat_messages.csv"
    await list_messages(chat_id, output_csv)

# Start the client and run the main function
with client:
    client.loop.run_until_complete(main())
