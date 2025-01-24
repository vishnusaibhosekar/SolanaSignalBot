from abc import ABC, abstractmethod

class TradeStep(ABC):
    """
    Abstract base class for a trade step.
    """

    @abstractmethod
    async def execute(self, executor):
        """
        Execute the trade step.
        Args:
            executor (TrojanExecutor): The executor instance executing the step.
        """
        pass

    @abstractmethod
    def verify(self, executor):
        """
        Verify if the step was successfully executed.
        Args:
            executor (TrojanExecutor): The executor instance verifying the step.
        """
        pass
