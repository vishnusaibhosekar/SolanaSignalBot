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
        self.csv_file = "trojan_message_logs.csv"  # Updated to match main.py log file name

        # Ensure log file has headers
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "sender_id", "channel_id", "message_id", "message_text", "is_reply", "replied_message_id", "event_type", "contract_address"])

    async def insta_buy(self, contract_address, token_ticker = None):
        """Perform an instant buy."""
        print(f"\nStarting instant buy for contract: {contract_address}\n")
        # self.current_trade.update({"in_progress": False, "contract_address": contract_address, "action": "buy"})
        # Log the sent message
        self.log_message_to_csv(
            event_type="sent",
            sender_id="0",
            channel_id=self.bot_username,
            message_id="0",
            message_text=contract_address,
            is_reply=False,
            replied_message_id=None,
            contract_address=contract_address
        )
        await self.client.send_message(self.bot_username, contract_address)

    def log_message_to_csv(self, event_type, sender_id, channel_id, message_id, message_text, is_reply, replied_message_id, contract_address):
        """Log messages to a CSV file."""
        try:
            with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().isoformat(),
                    sender_id,
                    channel_id,
                    message_id or "",
                    message_text or "",
                    is_reply,
                    replied_message_id if replied_message_id is not None else "",
                    event_type,
                    contract_address
                ])
        except Exception as e:
            print(f"Error logging message to CSV: {e}")
