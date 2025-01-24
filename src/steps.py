from models.trade_step import TradeStep
import asyncio

class SendMessageStep(TradeStep):
    def __init__(self, message):
        self.message = message

    async def execute(self, trade, executor):
        """
        Send a message using the executor's client.
        """
        await executor.client.send_message(executor.bot_username, self.message)

        # Log step progress
        executor.logger.log_trade(
            trade_id=trade.trade_id,
            contract_address=trade.contract_address,
            trade_type=trade.trade_type,
            status="message_sent",
            trade_step="SendMessageStep",
        )

class ClickButtonStep(TradeStep):
    def __init__(self, button_text, timeout=10):
        self.button_text = button_text
        self.timeout = timeout

    async def execute(self, executor):
        """
        Wait for an event with buttons and click the specified button.
        """
        # Wait for an event with buttons
        event = await executor.event_queue.get_event_with_filter(
            lambda e: hasattr(e.message, "buttons") and any(
                button.text.lower() == self.button_text.lower()
                for row in e.message.buttons for button in row
            ),
            timeout=self.timeout,
        )
        if not event:
            raise Exception("No event with matching button found within the timeout.")

        # Click the button
        for row in event.message.buttons:
            for button in row:
                if button.text.lower() == self.button_text.lower():
                    await button.click()
                    # TODO: update the trade logs
                    return

class VerifyBuySuccessStep(TradeStep):
    def __init__(self, timeout=10):
        self.timeout = timeout

    async def execute(self, trade, executor):
        """
        Wait for a buy success or failure event after sending the contract address.
        """
        executor.logger.log_trade(
            trade_id=trade.trade_id,
            contract_address=trade.contract_address,
            trade_type=trade.trade_type,
            status="waiting_for_event",
            trade_step="VerifyBuySuccessStep",
        )

        # Wait for the next relevant event
        event = await executor.event_queue.get_event_with_filter(
            lambda e: any(
                keyword in e.message.text.lower()
                for keyword in ["buy success", "insufficient balance", "token not found"]
            ),
            timeout=self.timeout,
        )

        if not event:
            raise Exception(f"Timeout waiting for trade response for contract: {self.contract_address}")

        # Extract event details
        message_text = event.message.text.lower()

        executor.logger.log_trade(
            trade_id=trade.trade_id,
            contract_address=trade.contract_address,
            trade_type=trade.trade_type,
            status="event_received",
            trade_step="VerifyBuySuccessStep",
        )

        # Print buttons if available
        if event.message.buttons:
            print("Event buttons:")
            for row in event.message.buttons:
                for button in row:
                    print(f" - {button.text}")

        # Check for specific outcomes and log accordingly
        if "buy success" in message_text and self.contract_address in message_text:
            executor.logger.log_trade(
                trade_id=trade.trade_id,
                contract_address=trade.contract_address,
                trade_type="insta_buy",
                status="success",
                trade_step="VerifyBuySuccessStep",
            )
        elif "insufficient balance" in message_text or "token not found" in message_text:
            executor.logger.log_trade(
                trade_id=trade.trade_id,
                contract_address=trade.contract_address,
                trade_type="insta_buy",
                status="failure",
                trade_step="VerifyBuySuccessStep",
            )
            raise Exception(f"Trade failed: {message_text}")
        else:
            raise Exception(f"Unexpected event message: {message_text}")
