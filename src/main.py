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
TRENCHES_CALLS_SENDER_ID_IN_TRENCHES_CHAT = int(os.getenv("TRENCHES_CALLS_SENDER_ID_IN_TRENCHES_CHAT"))
VISHNU_SENDER_ID = int(os.getenv("VISHNU_SENDER_ID"))
SIDDHARTH_SENDER_ID = int(os.getenv("SIDDHARTH_SENDER_ID"))

# Telegram client setup
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

# Allowed chat IDs (supergroups must start with -100)
chat_ids = [-1002367358385, -4650603403, -1002288621103]

@client.on(events.NewMessage(chats=chat_ids))
async def reply_handler(event):
    print(event.type)
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

    # Check if the reply is from RICKBOT to a message from TRENCHES_CALLS
    if reply_sender.id == RICKBOT_ID and original_sender.id == TRENCHES_CALLS_SENDER_ID_IN_TRENCHES_CHAT:
        print(f"Original message: {original_message.text}")
        print(f"Action triggered! Reply from {reply_sender.username} to TRENCHES_CALLS")

        # Extract contract address and token ticker from the reply message
        contract_address, token_ticker = extract_token_data(event.text or "")

        if contract_address:
            print(f"Detected contract address: {contract_address} ({token_ticker})")

            # Call the trade method
            try:
                trade_success = await automate_solana_trojan_bot(client, BOT_USERNAME, contract_address, token_ticker, "buy")
            except Exception as e:
                print(f"Error during trade execution: {e}")

async def main():
    # initialize_logs()
    print("Connected to Telegram!")
    print("Listening...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())