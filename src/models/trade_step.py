from abc import ABC, abstractmethod

class TradeStep(ABC):
    """
    Abstract base class for a trade step.
    """

    @abstractmethod
    async def execute(self, trade, executor):
        """
        Execute the trade step.
        Args:
            executor (TrojanExecutor): The executor instance executing the step.
        """
        pass
