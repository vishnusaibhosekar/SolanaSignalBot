from telethon import TelegramClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_API_ID = int(os.getenv("API_ID"))  # Ensure this is an integer
TELEGRAM_API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

# List of usernames to resolve
usernames = [
    "Nima2103", "simpin8ntpimpin", "ariannn74", "KTuck", "marcus_g_relius",
    "Juicebox10", "arcadesora", "zack178", "Jarled250", "alexem89", "PaddyCoke",
    "wesleywhb", "Mounir2507", "siddharthpeyyeti", "alexandrekozlo", "zillamix",
    "Flynn180", "JiggyStuntman", "Frenksuss", "Xodus_OG", "John8544",
    "ddjonesjr", "YousufStalin", "Minas098", "saylesscrypto", "clixtg",
    "kawaljit76", "satyaj2", "vnt_0x"
]

# Create a Telegram client instance
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH).start(phone=TELEGRAM_PHONE)

async def fetch_user_ids(usernames):
    """
    Fetch Telegram user IDs for the provided usernames.
    """
    user_ids = {}
    for username in usernames:
        try:
            user = await client.get_entity(username)
            user_ids[username] = user.id
            print(f"Username: {username}, ID: {user.id}")
        except Exception as e:
            user_ids[username] = None
            print(f"Failed to fetch ID for {username}: {e}")
    return user_ids

async def main():
    user_ids = await fetch_user_ids(usernames)

    # Save results to a file
    with open("telegram_user_ids.csv", "w") as f:
        f.write("username,user_id\n")
        for username, user_id in user_ids.items():
            f.write(f"{username},{user_id}\n")
    print("Results saved to 'telegram_user_ids.csv'")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
