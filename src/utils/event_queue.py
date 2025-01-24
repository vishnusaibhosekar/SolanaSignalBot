import asyncio

class EventQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_event(self, event):
        """
        Add a raw event to the queue.
        Args:
            event: Telethon event object.
        """
        await self.queue.put(event)

    async def get_event_with_filter(self, filter_func, timeout=None):
        """
        Get an event from the queue that matches the given filter.
        Args:
            filter_func (callable): A function that returns True for the desired event.
            timeout (int, optional): Time in seconds to wait for an event.
        Returns:
            Event or None: The matching event, or None if the timeout expires.
        """
        try:
            while True:
                event = await asyncio.wait_for(self.queue.get(), timeout)
                if filter_func(event):
                    return event
                else:
                    # Requeue the event if it doesn't match
                    await self.queue.put(event)
        except asyncio.TimeoutError:
            return None
