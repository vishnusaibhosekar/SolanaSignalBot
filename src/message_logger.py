from telethon import TelegramClient, events
from dotenv import load_dotenv
import asyncio
import os
from collections import deque
from utils.message_parser import extract_token_data
from trade_execution import automate_solana_trojan_bot

# create a config dict with chat_id, channel_id keys in config.py
from config import config

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

TROJAN_BOT_USERNAME = "solana_trojanbot"
UNIBOT_USERNAME = "unibot"

RICKBOT_ID = int(os.getenv("RICKBOT_ID"))
# VISI_CHAT_ID = int(os.getenv("VISI_CHAT_ID"))
# VISI_CHANNEL_ID = int(os.getenv("VISI_CHANNEL_ID"))
CHAT_ID = config["chat_id"]
CHANNEL_ID = config["channel_id"]

# Telegram client setup
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

# Initialize a queue for messages
message_queue = deque()
processing_lock = asyncio.Lock()

# Dictionary to track reply-waiting tasks
reply_tasks = {}

@client.on(events.NewMessage(chats=CHANNEL_ID))
async def new_message_handler(event):
    """
    Handles new messages in the channel.
    Adds them to the processing queue.
    """
    print(f"\nNew message in channel: {event.message.text}")
    message_queue.append(event.message)

    # Process messages in the queue one at a time
    async with processing_lock:
        while message_queue:
            current_message = message_queue.popleft()
            await process_message(current_message)

async def process_message(original_message):
    """
    Processes a single message from the channel.
    Waits for the forwarded message and listens for replies.
    """
    original_message_id = original_message.id
    forwarded_message = await wait_for_forwarded_message(original_message_id, 10)

    if forwarded_message:
        print(f"Forwarded message found in chat: {forwarded_message.text}")
        await listen_for_replies(forwarded_message)
    else:
        print("No forwarded message found within the timeout.")


async def wait_for_forwarded_message(original_message_id, timeout):
    """
    Wait for the forwarded message in chat for a specified timeout.
    Stops waiting as soon as the forwarded message is found.
    """
    try:
        forwarded_message = None
        event_received = asyncio.Event()  # Event to signal when the forwarded message is received

        @client.on(events.NewMessage(chats=CHAT_ID))
        async def forwarded_message_handler(event):
            nonlocal forwarded_message

            if event.message.fwd_from:
                fwd_from = event.message.fwd_from

                if (
                    f"-100{fwd_from.from_id.channel_id}" == str(CHANNEL_ID)
                    and fwd_from.channel_post == original_message_id
                ):

                    forwarded_message = event.message
                    event_received.set()  # Signal that the forwarded message is found

        try:
            # Wait for the forwarded message for up to `timeout` seconds
            await asyncio.wait_for(event_received.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            pass  # Timeout occurred, proceed without forwarded_message

        # Cleanup event handler
        client.remove_event_handler(forwarded_message_handler)
        return forwarded_message

    except Exception as e:
        print(f"Error while waiting for forwarded message: {e}")
        return None


async def listen_for_replies(forwarded_message):
    """
    Listen for replies to the forwarded message in Chat.
    Stops waiting as soon as a reply from Rickbot is found.
    Executes trades sequentially.
    """
    try:
        print(f"Listening for replies to forwarded message: {forwarded_message.text}")
        replies = []
        event_received = asyncio.Event()  # Event to signal when a reply is received

        @client.on(events.NewMessage(chats=CHAT_ID))
        async def reply_handler(event):
            nonlocal replies

            if event.is_reply:
                reply_to = await event.get_reply_message()
                if reply_to and reply_to.id == forwarded_message.id:
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
                print(f"Original message: {forwarded_message.text}")
                # print(f"Reply by RICKBOT: {reply.text}") # Don't print the reply to Rickbot - too spammy

                contract_address, token_ticker = extract_token_data(reply.text or "")

                if contract_address:
                    print(f"Detected contract address: {contract_address} ({token_ticker})")

                    # Ensure sequential execution of trades
                    async with processing_lock:
                        try:
                            trade_success = await automate_solana_trojan_bot(
                                client, TROJAN_BOT_USERNAME, contract_address, token_ticker, "buy"
                            )
                            if trade_success:
                                print(f"Trade executed successfully for {token_ticker}.")
                            else:
                                print(f"Trade execution failed for {token_ticker}.")
                        except Exception as e:
                            print(f"Error during trade execution: {e}")
        else:
            print("No replies from RICKBOT within the timeout for the message:")
            print(f"Original message: {forwarded_message.text}")

        # Cleanup event handler
        client.remove_event_handler(reply_handler)

    except Exception as e:
        print(f"Error while listening for replies: {e}")


async def main():
    print("Listening for new calls...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
