from listeners.base_listener import BaseListener
from telethon import events
from utils.logger import Logger

# Get the singleton logger instance
logger = Logger()

class TrojanListener(BaseListener):
    def __init__(self, client, event_queue, trojan_chat_id):
        """
        Initialize the TrojanListener with the Telegram client and trojan chat ID.
        """
        super().__init__(client)
        self.event_queue = event_queue
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

            logger.log_event(
                sender_id=sender.id if sender else None,
                channel_id=event.chat_id,
                message_id=event.message.id,
                message_text=event.message.text,
                is_reply=event.message.is_reply,
                replied_message_id=event.message.reply_to_msg_id if event.message.is_reply else None,
                event_type="new_message",
            )

            await self.event_queue.add_event(event)

        @self.client.on(events.MessageEdited(chats=self.trojan_chat_id))
        async def edited_message_handler(event):
            """
            Handles edited messages in the trojan chat and logs them only if the text was actually changed.
            """
            sender = await event.get_sender()

            logger.log_event(
                sender_id=sender.id if sender else None,
                channel_id=event.chat_id,
                message_id=event.message.id,
                message_text=event.message.text,
                is_reply=event.message.is_reply,
                replied_message_id=event.message.reply_to_msg_id if event.message.is_reply else None,
                event_type="message_edited",
            )

            await self.event_queue.add_event(event)
