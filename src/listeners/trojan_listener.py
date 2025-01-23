from listeners.base_listener import BaseListener
from telethon import TelegramClient, events
# from utils.logger import log_message, get_last_message_state  # Assuming log_message and get_last_message_state are utilities

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
        @self.client.on(events.NewMessage(chats=self.trojan_chat_id))
        async def new_message_handler(event):
            """
            Handles new messages in the trojan chat.
            Logs and processes the message.
            """
            channel_id = event.chat_id
            is_reply = event.message.is_reply
            replied_message_id = event.message.reply_to_msg_id if is_reply else None
            message_text = event.message.text

            # Log the new message
            log_message(channel_id, event.message.id, message_text, is_reply, replied_message_id, "new")

        @self.client.on(events.MessageEdited(chats=self.trojan_chat_id))
        async def edited_message_handler(event):
            """
            Handles edited messages in the trojan chat and logs them only if the text was actually changed.
            """
            message_id = event.message.id

            # Fetch the last state of the message from the logs
            last_text = get_last_message_state(message_id)

            # Compare the current text with the last logged state
            if last_text is not None and last_text.strip() == event.message.text.strip():
                return  # Skip logging if the text hasn't changed

            # Log the edited message
            channel_id = event.chat_id
            is_reply = event.message.is_reply
            replied_message_id = event.message.reply_to_msg_id if is_reply else None
            log_message(channel_id, event.message.id, event.message.text, is_reply, replied_message_id, "edit")
