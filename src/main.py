from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
from trade_execution import automate_solana_trojan_bot

# Load environment variables
load_dotenv()  # Debugging step to ensure it’s set correctly

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
BOT_USERNAME = "solana_trojanbot"


print(TELEGRAM_PHONE)

# Telegram client setup
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

# Allowed chat IDs (supergroups must start with -100)
chat_ids = [-1002367358385, -4650603403, -1002378664747]

# Log files
MESSAGE_LOG_FILE = "message_timeline_log.csv"
TRADE_LOG_FILE = "trade_log.csv"

# Initialize log files
def initialize_logs():
    if not os.path.exists(MESSAGE_LOG_FILE):
        with open(MESSAGE_LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "event_type", "message_id", "chat_id", "chat_name", "message_text"])
    if not os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "contract_address", "status", "amount", "price"])

def log_message_event(event_type, message_id, chat_id, chat_name, message_text):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(MESSAGE_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, event_type, message_id, chat_id, chat_name, message_text])

def log_trade_event(contract_address, status, amount=None, price=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(TRADE_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, contract_address, status, amount, price])

def detect_potential_address(message):
    words = message.split()
    for word in words:
        if len(word) > 20:
            return word
    return None

async def handle_message(event, event_type="new_message"):
    chat = await event.get_chat()
    chat_name = chat.title if hasattr(chat, "title") else "Private Chat"
    message_text = event.text or ""

    log_message_event(event_type, event.message.id, chat.id, chat_name, message_text)

    if event_type == "message_edited":
        return

    potential_address = detect_potential_address(message_text)
    if potential_address:
        print(f"Detected potential Solana contract address: {potential_address}")
        trade_success, amount, price = await automate_solana_trojan_bot(client, BOT_USERNAME, potential_address)
        log_trade_event(potential_address, "success" if trade_success else "failed", amount, price)

@client.on(events.NewMessage(chats=chat_ids))
async def new_message_handler(event):
    await handle_message(event, event_type="new_message")

@client.on(events.MessageEdited(chats=chat_ids))
async def edited_message_handler(event):
    await handle_message(event, event_type="message_edited")

async def main():
    initialize_logs()
    print("Connected to Telegram!")
    print("Listening...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
