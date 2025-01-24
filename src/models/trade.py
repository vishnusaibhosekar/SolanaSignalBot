# src/models/trade.py

class Trade:
    def __init__(self, trade_id, trade_type, wallet, trade_steps):
        """
        Initialize a Trade object.
        
        Args:
            trade_id (int): Unique identifier for the trade.
            trade_type (str): Type of the trade (e.g., "insta_buy", "create_limit_buy_order").
            wallet (str): Associated wallet for the trade.
            trade_steps (list): List of trade steps (instances of TradeStep).
        """
        self.trade_id = trade_id
        self.trade_type = trade_type
        self.wallet = wallet
        self.contract_address = None
        self.trade_steps = trade_steps
        self.status = "pending"  # Initial status
        self.logs = []  # Logs specific to this trade

    def add_log(self, message):
        """
        Add a log entry for this trade.
        """
        self.logs.append(message)

    def set_status(self, status):
        """
        Update the trade's status.
        Args:
            status (str): New status (e.g., "pending", "in_progress", "success", "failure").
        """
        self.status = status
