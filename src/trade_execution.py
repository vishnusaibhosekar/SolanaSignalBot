from telethon import events
import re

async def automate_solana_trojan_bot(client, bot_username, contract_address, amt=None):
    """
    Automates interactions with the Solana Trojan bot to execute a trade
    and extracts the SOL balance.
    
    Args:
        client (TelegramClient): The Telethon client instance.
        bot_username (str): The username of the bot to interact with.
        contract_address (str): The token's contract address to buy.
        amt (float): The amount of the token to trade (default: calculated dynamically).
    """
    print(f"Sending /start command to {bot_username}...")
    await client.send_message(bot_username, '/start')

    sol_balance = 0.0  # Initialize balance outside the handler

    @client.on(events.NewMessage(chats=bot_username))
    async def handle_bot_response(event):
        nonlocal sol_balance  # Allow modification of sol_balance from inside the handler
        message_text = event.message.message
        print(f"New message from {bot_username}: {message_text}")

        try:
            # Step 1: Extract SOL balance from the message
            if "Balance:" in message_text and sol_balance == 0.0:
                sol_balance = extract_sol_balance(message_text)
                print(f"Extracted SOL Balance: {sol_balance}")

            # Step 2: Look for the "Buy" button and click it
            if event.message.buttons:
                for row in event.message.buttons:
                    for button in row:
                        print(f"Button Text: {button.text}")
                        if "SOL ✏️" in button.text:
                            print("Clicking the 'SOL ✏️' button...")
                            await button.click()
                            return  # Wait for the bot's next response
                        if button.text.lower() == "buy":
                            print("Clicking the 'Buy' button...")
                            await button.click()
                            return  # Wait for the bot's next response

            # Step 3: Respond with the token contract address when prompted
            if "enter a token symbol or address to buy" in message_text.lower():
                print(f"Sending contract address: {contract_address}")
                await client.send_message(bot_username, contract_address)
                return

            # Step 4: Respond with the amount when prompted
            if "enter sol amount" in message_text.lower():
                # Calculate amount dynamically if not provided
                if amt is None:
                    amt = round(sol_balance * 0.01, 4)  # Calculate 1% of SOL balance, rounded to 4 decimals
                print(f"Sending amount: {amt}")
                await client.send_message(bot_username, str(amt))
                print("Trade execution completed!")
                return

        except Exception as e:
            print(f"Error processing bot response: {e}")

def extract_sol_balance(message_text):
    """
    Extracts the SOL balance from the bot's message text.
    
    Args:
        message_text (str): The text of the message.
    
    Returns:
        float: The extracted SOL balance, or 0.0 if not found.
    """
    try:
        # Use regex to find the balance line
        match = re.search(r"Balance:\s([\d.]+)\sSOL", message_text)
        if match:
            return float(match.group(1))
    except Exception as e:
        print(f"Error extracting SOL balance: {e}")
    return 0.0
