import csv
import os
from datetime import datetime, timezone

class Logger:
    _instance = None  # Singleton instance
    LOG_DIR = "logs"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initialize the logger by creating the logs directory.
        """
        if not os.path.exists(self.LOG_DIR):
            os.makedirs(self.LOG_DIR, exist_ok=True)
            print(f"Logs directory created: {self.LOG_DIR}")

    def initialize_event_log_file(self, log_file):
        """
        Ensure the log file exists and has the correct headers.
        """
        if not os.path.exists(log_file):
            print(f"Creating log file: {log_file}")
            with open(log_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "sender_id", "channel_id", "message_id", "message_text", "is_reply", "replied_message_id", "event_type"])

    def initialize_trade_log_file(self, log_file):
        """
        Ensure the log file exists and has the correct headers.
        """
        if not os.path.exists(log_file):
            print(f"Creating log file: {log_file}")
            with open(log_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "trade_id", "contract_address", "trade_type", "status", "trade_step"])

    def log_event(self, sender_id, channel_id, message_id, message_text, is_reply, replied_message_id, event_type):
        """
        Logs a message to the specified log file with a unique event_id.
        """
        log_file = os.path.join(self.LOG_DIR, "trojan_event_logs.csv")
        self.initialize_event_log_file(log_file)  # Ensure the file has headers

        try:
            with open(log_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now(timezone.utc).isoformat(),
                    sender_id,
                    channel_id,
                    message_id,
                    message_text,
                    is_reply,
                    replied_message_id or "",
                    event_type,
                ])
        except Exception as e:
            print(f"Error writing to log file {log_file}: {e}")

    def log_trade(self, trade_id, contract_address, trade_type, status, trade_step=None):
        """
        Log trade information to a specific log file.
        
        Args:
        trade_id (int): Unique ID for the trade.
        contract_address (str): Address of the token being traded.
        trade_type (str): Type of trade (e.g., insta_buy).
        status (str): Current status of the trade (e.g., started, success, failure).
        trade_step (str): Optional step name for granular logging.
        """
        log_file = os.path.join(self.LOG_DIR, "trojan_trades.csv")
        self.initialize_trade_log_file(log_file)  # Ensure the file has headers

        try:
            with open(log_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now(timezone.utc).isoformat(),  # Timestamp
                    trade_id,  # Trade ID
                    contract_address,  # Contract address
                    trade_type,  # Trade type
                    status,  # Trade status
                    trade_step or "",  # Add trade_step or empty string if not provided
                ])
        except Exception as e:
            print(f"Error logging trade to {log_file}: {e}")
