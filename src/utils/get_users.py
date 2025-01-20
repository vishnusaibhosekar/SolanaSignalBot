from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChannel
from dotenv import load_dotenv
import asyncio
import os
import re
import pandas as pd

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = os.getenv("API_ID")
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
group_id = -1002174499123  # Replace with your group's ID
bot_id = 5887832843  # Bot's ID

# Create a client instance
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

# Regular expression to parse bot replies
reply_pattern = re.compile(
    r"@(?P<username>\w+)\s+Win Rate: (?P<win_rate>\d+\.\d+)%\s+Total Calls: (?P<total_calls>\d+)\s+Average X Per Call: (?P<avg_x>\d+\.\d+)"
)

# List to store extracted data
results = []

async def fetch_users_and_message_bot():
    # Get the group entity
    group = await client.get_entity(group_id)

    # Fetch participants
    participants = await client.get_participants(group)

    print(f"Users in group '{group.title}':")
    for user in participants:
        if user.username:
            print(f"Sending message for @{user.username}")
            message = f"/winrate @{user.username}"
            await client.send_message(bot_id, message)
            # Wait for the bot's reply
            await asyncio.sleep(0.5)

@client.on(events.NewMessage(from_users=bot_id))
async def handle_bot_reply(event):
    # Extract data from bot reply
    match = reply_pattern.search(event.raw_text)
    if match:
        results.append(match.groupdict())
        print(f"Extracted data: {match.groupdict()}")

async def main():
    # Fetch users and send messages to the bot
    await fetch_users_and_message_bot()

    # Wait for all replies to be handled
    await asyncio.sleep(10)  # Wait for a buffer period for all replies to arrive

    # Save results to a CSV file
    if results:
        df = pd.DataFrame(results)
        df.to_csv("winrate_results.csv", index=False)
        print("Data saved to winrate_results.csv")
    else:
        print("No data extracted")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
