from abc import ABC, abstractmethod

class TradeExecutor(ABC):
    """
    Abstract base class for a trade executor.
    """

    @abstractmethod
    async def execute_trade(self, trade):
        """
        Execute a trade by processing its steps.
        Args:
            trade (Trade): The trade to execute.
        """
        pass
