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

    def initialize_log_file(self, log_file):
        """
        Ensure the log file exists and has the correct headers.
        """
        if not os.path.exists(log_file):
            print(f"Creating log file: {log_file}")
            with open(log_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["event_id", "timestamp", "sender_id", "channel_id", "message_id", "message_text", "is_reply", "replied_message_id", "event_type"])

    def get_next_event_id(self, log_file):
        """
        Calculate the next event_id based on the current log file contents.
        """
        if not os.path.exists(log_file):
            return 1  # Start at 1 if the file doesn't exist

        try:
            with open(log_file, mode="r") as file:
                rows = list(csv.DictReader(file))
                if rows:
                    last_event = rows[-1]
                    return int(last_event["event_id"]) + 1
        except Exception as e:
            print(f"Error calculating next event_id for {log_file}: {e}")
        return 1  # Fallback to 1 if there's an error

    def log_event(self, log_file, sender_id, channel_id, message_id, message_text, is_reply, replied_message_id, event_type):
        """
        Logs a message to the specified log file with a unique event_id.
        """
        self.initialize_log_file(log_file)  # Ensure the file has headers
        event_id = self.get_next_event_id(log_file)

        try:
            with open(log_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    event_id,
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

    def get_last_message_state(self, log_file, message_id):
        """
        Fetches the last logged state of a message from the specified log file.
        """
        try:
            with open(log_file, mode="r") as file:
                rows = list(csv.DictReader(file))
                for row in reversed(rows):  # Iterate from the latest
                    if int(row["message_id"]) == message_id:
                        return row["message_text"]
        except Exception as e:
            print(f"Error fetching message state from {log_file}: {e}")
        return None
