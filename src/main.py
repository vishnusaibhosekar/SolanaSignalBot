from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
from trade_execution import automate_solana_trojan_bot  # Import the function

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
BOT_USERNAME = "solana_trojanbot"

# Telegram client setup
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

chat_ids = [-1002367358385, -4650603403]

# Log files
MESSAGE_LOG_FILE = "message_timeline_log.csv"
TRADE_LOG_FILE = "trade_log.csv"

# Initialize log files
def initialize_logs():
    # Initialize message log
    if not os.path.exists(MESSAGE_LOG_FILE):
        with open(MESSAGE_LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "event_type", "message_id", "chat_id", "sender_id",
                             "sender_name", "chat_name", "message_text"])

    # Initialize trade log
    if not os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "contract_address", "status"])

# Log message events
def log_message_event(event_type, message_id, chat_id, sender_id, sender_name, chat_name, message_text):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # More readable timestamp
    with open(MESSAGE_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, event_type, message_id, chat_id, sender_id, sender_name, chat_name, message_text])

# Log trade events
def log_trade_event(contract_address, status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # More readable timestamp
    with open(TRADE_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, contract_address, status])
        
def detect_potential_address(message):
    """
    Detects words longer than 20 characters in a message.
    """
    words = message.split()
    for word in words:
        if len(word) > 20:
            return word
    return None

async def handle_message(event, event_type="new_message"):
    """
    Handles both new and edited messages.
    """
    # Fetch sender information
    sender = await event.get_sender()
    sender_name = sender.first_name if sender else "Unknown"
    sender_id = sender.id if sender else "Unknown"

    # Fetch chat information
    chat = await event.get_chat()
    chat_name = chat.title if hasattr(chat, "title") else "Private Chat"

    # Fetch the message text
    message_text = event.text or ""

    # Log the event
    log_message_event(event_type, event.message.id, chat.id, sender_id, sender_name, chat_name, message_text)

    # Detect potential contract address
    potential_address = detect_potential_address(message_text)
    if potential_address:
        print(f"Detected potential Solana contract address: {potential_address}")

        # Trigger Solana Trojan bot automation
        trade_success = await automate_solana_trojan_bot(client, BOT_USERNAME, potential_address)

        # Log the trade
        if trade_success:
            log_trade_event(potential_address, "success")
            print(f"Trade successful for contract: {potential_address}.")
        else:
            log_trade_event(potential_address, "failed")
            print(f"Trade failed for contract: {potential_address}.")

@client.on(events.NewMessage(chats=chat_ids))
async def new_message_handler(event):
    """Handles new messages."""
    await handle_message(event, event_type="new_message")

@client.on(events.MessageEdited(chats=chat_ids))
async def edited_message_handler(event):
    """Handles edited messages."""
    await handle_message(event, event_type="message_edited")

async def main():
    """Start the Telegram client."""
    initialize_logs()
    print("Connected to Telegram!")
    print("Listening...")
    await client.run_until_disconnected()

# Start the client and main function
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
