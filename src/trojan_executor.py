import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
import csv
from datetime import datetime
import re

class TrojanExecutor:
    def __init__(self, client, bot_username):
        self.client = client
        self.bot_username = bot_username
        self.current_trade = {"in_progress": False, "contract_address": None, "action": None}
        self.event_listeners_registered = False
        self.csv_file = "bot_messages.csv"

        # Message queue for processing trade actions
        # self.message_queue = asyncio.Queue()
        # self.processing_task = asyncio.create_task(self.process_message_queue())

        # Ensure log file has headers
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "event_type", "message_id", "sender_id", "message_text"])

        # Register event listeners on initialization
        self.register_event_listeners()

    def register_event_listeners(self):
        """Register event listeners for new and edited messages."""
        if not self.event_listeners_registered:
            @self.client.on(events.NewMessage(chats=self.bot_username))
            async def handle_new_message(event):
                await self.handle_bot_response(event, "new_message")

            @self.client.on(events.MessageEdited(chats=self.bot_username))
            async def handle_edited_message(event):
                await self.handle_bot_response(event, "edited_message")

            self.event_listeners_registered = True

    async def handle_bot_response(self, event, event_type):
        """Handle bot responses and process trade state."""
        message_text = event.message.message
        sender_id = event.sender_id
        self.log_message_to_csv(event_type, event.message.id, sender_id, message_text)

        try:
            # If a trade is in progress, handle success messages
            if self.current_trade["in_progress"]:
                if "Buy Success" in message_text or "Sell Success" in message_text:
                    print("Trade executed successfully!")
                    self.current_trade = {"in_progress": False, "contract_address": None, "action": None}
                return

            # Process trade initiation
            if "Balance:" in message_text and event_type == "new_message":
                sol_balance = self.extract_sol_balance(message_text)
                print(f"Extracted SOL Balance: {sol_balance}\n")

            if event.message.buttons:
                for row in event.message.buttons:
                    print(" | ".join(button.text for button in row))
                    for button in row:
                        if button.text.lower() == self.current_trade.get("action", ""):
                            print(f"Button clicked: {button.text}")
                            await button.click()
                            return

            if "enter a token symbol or address" in message_text.lower():
                print(f"Sending contract address: {self.current_trade['contract_address']}\n")
                await self.client.send_message(self.bot_username, self.current_trade["contract_address"])
                self.current_trade["in_progress"] = True
                return

        except Exception as e:
            print(f"Error processing bot response: {e}")
            self.current_trade = {"in_progress": False, "contract_address": None, "action": None}

    async def insta_buy(self, contract_address, percentage, token_ticker = None):
        """Perform an instant buy."""
        print(f"\nStarting instant buy for {percentage}% of portfolio for contract: {contract_address}\n")
        self.current_trade.update({"in_progress": False, "contract_address": contract_address, "action": "buy"})
        await self.client.send_message(self.bot_username, '/start')
        self.log_message_to_csv("sent", None, self.client.session.user_id, "/start")

    def extract_sol_balance(self, message_text):
        """Extract the SOL balance from a message."""
        try:
            match = re.search(r"Balance:\s([\d.]+)\sSOL", message_text)
            if match:
                return float(match.group(1))
        except Exception as e:
            print(f"Error extracting SOL balance: {e}")
        return 0.0

    def log_message_to_csv(self, event_type, message_id, sender_id, message_text):
        """Log messages to a CSV file."""
        try:
            with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().isoformat(),
                    event_type,
                    message_id or "",
                    sender_id or "",
                    message_text or ""
                ])
        except Exception as e:
            print(f"Error logging message to CSV: {e}")

async def load_env_and_initialize():
    """Load environment variables and initialize the Telegram client."""
    from dotenv import load_dotenv
    import os
    from telethon import TelegramClient

    load_dotenv()

    TELEGRAM_API_ID = os.getenv("API_ID")
    TELEGRAM_API_HASH = os.getenv("API_HASH")
    SESSION_NAME = os.getenv("SESSION_NAME")
    TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
    TROJAN_BOT_USERNAME = os.getenv("TROJAN_BOT_USERNAME", "solana_trojanbot")

    # Create client and await the start coroutine
    client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start(phone=TELEGRAM_PHONE)

    # Initialize TrojanExecutor after the client is fully started
    executor = TrojanExecutor(client, TROJAN_BOT_USERNAME)

    return client, executor
