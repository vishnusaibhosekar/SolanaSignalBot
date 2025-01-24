import os
import asyncio
from dotenv import load_dotenv
from client import TelegramClientSingleton
from listeners.trojan_listener import TrojanListener
from executors.trojan_executor import TrojanExecutor
from utils.event_queue import EventQueue
from models.trade import Trade
from steps import SendMessageStep, ClickButtonStep, VerifyBuySuccessStep

# Load environment variables
load_dotenv()

TROJAN_CHAT_ID = int(os.getenv("TROJAN_CHAT_ID"))
BOT_USERNAME = "solana_trojanbot"

async def main():
    event_queue = EventQueue()
    client = await TelegramClientSingleton.get_instance()

    # Initialize the listener
    trojan_listener = TrojanListener(client, event_queue, TROJAN_CHAT_ID)
    await trojan_listener.register_listener()
    print("TrojanListener is active...")

    # Initialize the executor
    executor = TrojanExecutor(bot_username=BOT_USERNAME, event_queue=event_queue)
    await executor.init_client()  # Ensure client is initialized

    # Define a trade
    trade_steps = [
        SendMessageStep(message="token_contract_address"),  # Step 1: Send contract address
        VerifyBuySuccessStep(timeout=10),  # Step 2: Wait for success/failure
    ]
    trade = Trade(trade_id=1, trade_type="insta_buy", contract_address="token_contract_address", wallet="trojan_wallet", trade_steps=trade_steps)

    # Execute the trade
    await executor.execute_trade(trade)

    print(f"Trade {trade.trade_id} completed with status: {trade.status}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
