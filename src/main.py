from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
from trade_execution import automate_solana_trojan_bot
from utils.message_filters import apply_filters
from utils.message_parser import extract_token_data

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

BOT_USERNAME = "solana_trojanbot"

RICKBOT_ID = int(os.getenv("RICKBOT_ID"))
TRENCHES_CALLS_SENDER_ID = int(os.getenv("TRENCHES_CALLS_SENDER_ID"))
VISHNU_SENDER_ID = int(os.getenv("VISHNU_SENDER_ID"))
SIDDHARTH_SENDER_ID = int(os.getenv("SIDDHARTH_SENDER_ID"))

# Telegram client setup
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

# Allowed chat IDs (supergroups must start with -100)
chat_ids = [-1002367358385, -4650603403, -1002378664747, -1002378664747]

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

async def handle_message(event, event_type="new_message"):
    chat = await event.get_chat()
    chat_name = chat.title if hasattr(chat, "title") else "Private Chat"
    message_text = event.text or ""

    sender = await event.get_sender()
    sender_name = sender.username if sender.username else sender.first_name

    if not apply_filters(event.sender_id, message_text):
        print(f"Message from sender {sender_name} (ID: {event.sender_id}) filtered out.")
        return

    log_message_event(event_type, event.message.id, chat.id, chat_name, message_text)

    # if event_type == "message_edited":
    #     return

    contract_address, token_ticker = extract_token_data(message_text)

    if contract_address:
        print(f"Detected contract address: {contract_address} ({token_ticker})")
        # trade_success = await automate_solana_trojan_bot(client, BOT_USERNAME, contract_address, token_ticker, "buy")
        # log_trade_event(contract_address, "success" if trade_success else "failed", amount, price)

@client.on(events.NewMessage(chats=chat_ids))
async def new_message_handler(event):
    await handle_message(event, event_type="new_message")

@client.on(events.NewMessage(chats=chat_ids))
async def reply_handler(event):
    # Check if the message is a reply
    if not event.is_reply:
        return
    
    # Get the original message
    original_message = await event.get_reply_message()
    if not original_message:
        return
    
    # Get sender details
    original_sender = await original_message.get_sender()
    reply_sender = await event.get_sender()
    
    # Check if the reply is from RICKBOT to a message from VISHNU
    if reply_sender.id == RICKBOT_ID and original_sender.id == VISHNU_SENDER_ID:
        print(f"Original message: {original_message.text}")
        print(f"Action triggered! Reply from {reply_sender.username} to {original_sender.username}")
        
        # Extract contract address and token ticker from the reply message
        contract_address, token_ticker = extract_token_data(event.text or "")
        
        if contract_address:
            print(f"Detected contract address: {contract_address} ({token_ticker})")
            
            # Call the trade method
            try:
                trade_success = await automate_solana_trojan_bot(client, BOT_USERNAME, contract_address, token_ticker, "buy")
                # log_trade_event(contract_address, "success" if trade_success else "failed", amount, price)
            except Exception as e:
                print(f"Error during trade execution: {e}")

# @client.on(events.MessageEdited(chats=chat_ids))
# async def edited_message_handler(event):
#     await handle_message(event, event_type="message_edited")

async def main():
    initialize_logs()
    print("Connected to Telegram!")
    print("Listening...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
