from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import csv
from utils.message_filters import apply_filters
from utils.message_parser import parse_message
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

# Allowed chat IDs (supergroups must start with -100)
chat_ids = [-1002367358385, -4650603403]

# CSV file to track executed trades
TRADE_LOG_FILE = "trade_log.csv"

# Ensure the trade log file exists
def initialize_trade_log():
    if not os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["contract_address"])

# Check if a trade has already been executed
def is_duplicate_trade(contract_address):
    with open(TRADE_LOG_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        for row in reader:
            if row[0] == contract_address:
                return True
    return False

# Log a successful trade
def log_trade(contract_address):
    with open(TRADE_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([contract_address])

def detect_potential_address(message):
    """
    Detects words longer than 20 characters in a message.
    """
    words = message.split()
    for word in words:
        if len(word) > 20:
            return word
    return None

async def handle_message(event):
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

    print("-------------------------------------")
    print(f"Message from {sender_name} [{sender_id}] in {chat_name}: {message_text}")
    print("-------------------------------------")

    # Detect potential contract address
    potential_address = detect_potential_address(message_text)
    if potential_address:
        print(f"Detected potential Solana contract address: {potential_address}")

        # Check for duplicate trades
        if is_duplicate_trade(potential_address):
            print(f"Duplicate trade detected for contract: {potential_address}. Skipping execution.")
            return

        # Trigger Solana Trojan bot automation
        print(f"Automating Solana bot interaction for contract: {potential_address}")
        trade_success = await automate_solana_trojan_bot(client, BOT_USERNAME, potential_address)

        # Log the trade if successful
        if trade_success:
            print(f"Trade successful for contract: {potential_address}. Logging trade.")
            log_trade(potential_address)
        else:
            print(f"Trade failed for contract: {potential_address}. Not logging.")

@client.on(events.NewMessage(chats=chat_ids))
async def new_message_handler(event):
    """Handles new messages."""
    await handle_message(event)

@client.on(events.MessageEdited(chats=chat_ids))
async def edited_message_handler(event):
    """Handles edited messages."""
    await handle_message(event)

async def main():
    """Start the Telegram client."""
    initialize_trade_log()
    print("Connected to Telegram!")
    print("Listening...")
    await client.run_until_disconnected()

# Start the client and main function
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
