import asyncio
from executors.trade_executor import TradeExecutor
from utils.logger import Logger

class TrojanExecutor(TradeExecutor):
    def __init__(self, client, bot_username):
        """
        Initialize the TrojanExecutor.

        Args:
            client (TelegramClient): Telegram client for interacting with the bot.
            bot_username (str): Bot username to interact with.
        """
        self.client = client
        self.bot_username = bot_username
        self.logger = Logger()

    async def execute_trade(self, trade):
        """
        Execute a trade by processing its steps sequentially.

        Args:
            trade (Trade): The trade to execute.
        """
        self.logger.log_event(
            log_file="logs/trojan_event_logs.csv",  # Log trade execution
            sender_id=None,  # Trade-level logging
            channel_id=None,
            message_id=None,
            message_text=None,
            is_reply=False,
            replied_message_id=None,
            event_type=f"Trade {trade.trade_id} started: {trade.trade_type}",
        )

        # Process each step
        for step in trade.trade_steps:
            try:
                # Execute the step
                await step.execute(self)

                # Verify the step
                if not step.verify(self):
                    raise Exception(f"Step verification failed for trade {trade.trade_id}")

            except Exception as e:
                # Log failure and set trade status
                self.logger.log_event(
                    log_file="logs/trojan_event_logs.csv",
                    sender_id=None,
                    channel_id=None,
                    message_id=None,
                    message_text=str(e),
                    is_reply=False,
                    replied_message_id=None,
                    event_type=f"Trade {trade.trade_id} failed",
                )
                trade.set_status("failure")
                trade.add_log(f"Error: {e}")
                return  # Stop processing further steps

        # Mark trade as successful
        trade.set_status("success")
        self.logger.log_event(
            log_file="logs/trojan_event_logs.csv",
            sender_id=None,
            channel_id=None,
            message_id=None,
            message_text=None,
            is_reply=False,
            replied_message_id=None,
            event_type=f"Trade {trade.trade_id} completed successfully",
        )
