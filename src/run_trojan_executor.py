import asyncio
from trojan_executor import load_env_and_initialize

async def start_trojan_executor():
    """Start the TrojanExecutor and keep it running."""
    client, executor = await load_env_and_initialize()

    print("TrojanExecutor is now running. Listening for messages...")
    try:
        # Keep the client running to listen for events
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Error occurred while running TrojanExecutor: {e}")
    finally:
        # Ensure client disconnects gracefully on shutdown
        await client.disconnect()
        print("TrojanExecutor has been stopped.")

if __name__ == "__main__":
    asyncio.run(start_trojan_executor())
