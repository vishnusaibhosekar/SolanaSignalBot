import csv
from datetime import datetime, timezone
from telethon import TelegramClient, events
from dotenv import load_dotenv
import asyncio
import os
from utils.message_parser import extract_token_data
from trojan_executor import TrojanExecutor

# create a config dict with chat_id, channel_id keys in config.py
from config import trenches_config, visi_config, SHITCOIN_COMMUNITY_CALLS_ID

config = trenches_config

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = os.getenv("API_ID")
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

TROJAN_BOT_USERNAME = "solana_trojanbot"
UNIBOT_USERNAME = "unibot"
TROJAN_CHAT_ID = os.getenv("TROJAN_CHAT_ID")

RICKBOT_ID = int(os.getenv("RICKBOT_ID"))
SECTBOT_ID = int(os.getenv("SECTBOT_ID"))
CHANNEL_IDS = config["channel_ids"]
FORWARD_CHAT_ID = config["forward_chat_id"]

GOATED_CALLERS_SENDER_IDS = [2119724331,1223694233,409154569,1338353807,964598469,769169133,1535262638,493872071,5484082105,1397332595,777844680,1797023625,1832350846,2131915710,5296498018,5542088802,1605472926,223721205,408193103,993953512,321994950,1777312783,1616484060,5395602026]

# CSV log file path
LOG_FILE = "message_logs.csv"

# Ensure log file has headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "channel_id", "message_id", "message_text", "is_reply", "replied_message_id", "event_type"])

# Telegram client setup
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

# Initialize TrojanExecutor
executor = TrojanExecutor(client, TROJAN_BOT_USERNAME)

def get_last_message_state(message_id):
    """
    Fetch the last logged state of a message from the CSV log file.
    Prioritizes the latest message (greatest message ID) for efficiency.
    Returns the message text if found, or None if not found.
    """
    try:
        with open(LOG_FILE, mode="r") as file:
            rows = list(csv.DictReader(file))  # Read all rows into a list
            for row in reversed(rows):  # Iterate from the latest (greatest ID)
                if int(row["message_id"]) == message_id:
                    return row["message_text"]
    except Exception as e:
        print(f"Error while fetching message state: {e}")
    return None

def log_message(channel_id, message_id, message_text, is_reply, replied_message_id, event_type):
    """
    Logs message details to a CSV file.
    """
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),  # Use timezone-aware UTC datetime
            channel_id,
            message_id,
            message_text,
            is_reply,
            replied_message_id if replied_message_id is not None else "",
            event_type
        ])

@client.on(events.NewMessage(chats=CHANNEL_IDS))
async def new_message_handler(event):
    """"
    Handles new messages in the channel.
    Forwards the message text to the forward chat and processes replies there.
    """
    channel_id = event.chat_id
    is_reply = event.message.is_reply
    replied_message_id = event.message.reply_to_msg_id if is_reply else None
    message_text = event.message.text

    # Handle shitcoins community calls case
    if channel_id == SHITCOIN_COMMUNITY_CALLS_ID:
        sender = await event.get_sender()
        if sender.id == SECTBOT_ID and event.message.is_reply:
            # Fetch the original sender from the replied-to message
            replied_message = await client.get_messages(channel_id, ids=replied_message_id)
            original_sender = await replied_message.get_sender()

            # Only proceed if the original sender ID is in GOATED_CALLERS
            if not original_sender.id in GOATED_CALLERS_SENDER_IDS:
                return
        else:
            return

    # Forward the message
    await forward_message(client, FORWARD_CHAT_ID, message_text)

    # Log the new message
    # TODO: add a primary key event_id in the log
    log_message(channel_id, event.message.id, message_text, is_reply, replied_message_id, "new")

    # Listen for replies in FORWARD_CHAT_ID
    await listen_for_replies(event.message.text)

async def forward_message(client, forward_chat_id, message_text):
    """
    Forwards a message's text in forward_chat_id.
    """
    try:
        await client.send_message(forward_chat_id, message_text)
        # print(f"Message forwarded to chat {forward_chat_id}: {message_text}")
    except Exception as e:
        print(f"Error while forwarding message: {e}")

@client.on(events.MessageEdited(chats=CHANNEL_IDS))
async def edited_message_handler(event):
    """
    Handles edited messages in the channel and logs them only if the text was actually changed.
    """
    message_id = event.message.id

    # Fetch the last state of the message from the logs
    last_text = get_last_message_state(message_id)

    # Compare the current text with the last logged state
    if last_text is not None and last_text.strip() == event.message.text.strip():
        return

    # Log the edited message
    channel_id = event.chat_id
    is_reply = event.message.is_reply
    replied_message_id = event.message.reply_to_msg_id if is_reply else None
    log_message(channel_id, event.message.id, event.message.text, is_reply, replied_message_id, "edit")

async def listen_for_replies(forwarded_message_text):
    """
    Listen for replies to the forwarded message in Chat.
    Stops waiting as soon as a reply from Rickbot is found.
    Executes trades sequentially.
    """
    try:
        print(f"Listening for replies in FORWARD_CHAT_ID: {FORWARD_CHAT_ID}")
        replies = []
        event_received = asyncio.Event()  # Event to signal when a reply is received

        @client.on(events.NewMessage(chats=FORWARD_CHAT_ID))
        async def reply_handler(event):
            nonlocal replies

            if event.is_reply:
                reply_to = await event.get_reply_message()
                if reply_to and reply_to.text.strip() == forwarded_message_text.strip():
                    sender = await event.get_sender()
                    if sender.id == RICKBOT_ID:
                        replies.append(event)
                        event_received.set()  # Signal that a reply from Rickbot is found

        try:
            # Wait for replies for up to `timeout` seconds
            await asyncio.wait_for(event_received.wait(), timeout=10)
        except asyncio.TimeoutError:
            pass  # Timeout occurred, proceed without replies

        # Process the reply if found
        if replies:
            for reply in replies:
                # print(f"Reply by RICKBOT: {reply.text}") # Don't print the reply to Rickbot - too spammy

                contract_address, token_ticker = extract_token_data(reply.text or "")

                if contract_address:
                    print(f"Detected contract address: {contract_address} ({token_ticker})")

                    # Ensure sequential execution of trades
                    try:
                        await executor.insta_buy(contract_address, token_ticker)
                    except Exception as e:
                        print(f"Error during trade execution: {e}")
        else:
            print("No replies from RICKBOT within the timeout for the message:")
            print(f"Original message: {forwarded_message_text}")

        # Cleanup event handler
        client.remove_event_handler(reply_handler)

    except Exception as e:
        print(f"Error while listening for replies: {e}")

async def main():
    print("Listening for new calls with config: " + str(config))
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
