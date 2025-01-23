import os
from listeners.base_listener import BaseListener
from telethon import events
from utils.logger import Logger

# Get the singleton logger instance
logger = Logger()

# Define log file for Trojan events
TROJAN_EVENTS_LOG_FILE = os.path.join(Logger.LOG_DIR, "trojan_event_logs.csv")

class TrojanListener(BaseListener):
    def __init__(self, client, trojan_chat_id):
        """
        Initialize the TrojanListener with a Telegram client and the trojan chat ID.
        """
        super().__init__(client)
        self.trojan_chat_id = trojan_chat_id

    async def register_listener(self):
        """
        Register the event handlers for new and edited messages in the trojan chat.
        """
        print("Registering listeners in TrojanListener")

        @self.client.on(events.NewMessage(chats=self.trojan_chat_id))
        async def new_message_handler(event):
            """
            Handles new messages in the trojan chat.
            Logs and processes the message.
            """
            sender = await event.get_sender()
            sender_id = sender.id if sender else None
            channel_id = event.chat_id
            is_reply = event.message.is_reply
            replied_message_id = event.message.reply_to_msg_id if is_reply else None
            message_text = event.message.text

            logger.log_event(
                TROJAN_EVENTS_LOG_FILE,
                sender_id,
                channel_id,
                event.message.id,
                message_text,
                is_reply,
                replied_message_id,
                "new"
            )

        @self.client.on(events.MessageEdited(chats=self.trojan_chat_id))
        async def edited_message_handler(event):
            """
            Handles edited messages in the trojan chat and logs them only if the text was actually changed.
            """
            sender = await event.get_sender()
            sender_id = sender.id if sender else None
            message_id = event.message.id
            channel_id = event.chat_id

            # Fetch the last state of the message from the logs
            last_text = logger.get_last_message_state(TROJAN_EVENTS_LOG_FILE, message_id)

            # Compare the current text with the last logged state
            if last_text is not None and last_text.strip() == event.message.text.strip():
                print("Message text unchanged. Skipping log.")
                return  # Skip logging if the text hasn't changed

            logger.log_event(
                TROJAN_EVENTS_LOG_FILE,
                sender_id,
                channel_id,
                message_id,
                event.message.text,
                event.message.is_reply,
                event.message.reply_to_msg_id if event.message.is_reply else None,
                "edit"
            )
