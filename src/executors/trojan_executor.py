from executors.trade_executor import TradeExecutor
from utils.logger import Logger
from client import TelegramClientSingleton

class TrojanExecutor(TradeExecutor):
    def __init__(self, bot_username, event_queue):
        """
        Initialize the TrojanExecutor.

        Args:
            bot_username (str): Bot username to interact with.
            event_queue (EventQueue): Shared event queue.
        """
        self.bot_username = bot_username
        self.event_queue = event_queue
        self.logger = Logger()

    async def init_client(self):
        """
        Initialize the Telegram client asynchronously.
        """
        self.client = await TelegramClientSingleton.get_instance()

    async def execute_trade(self, trade):
        """
        Execute a trade by processing its steps sequentially.

        Args:
            trade (Trade): The trade to execute.
        """
        # Log trade start using log_trade
        self.logger.log_trade(
            trade_id=trade.trade_id,
            contract_address=trade.contract_address,
            trade_type=trade.trade_type,
            status="started"
        )

        trade.set_status("in_progress")

        # Process each step in the trade
        for step in trade.trade_steps:
            try:
                # Execute the step
                await step.execute(trade, self)
            except Exception as e:
                print("Exception while executing step:", e)
                trade.set_status("failure")
                return

