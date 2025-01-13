from telethon import events
import re

async def automate_solana_trojan_bot(client, bot_username, contract_address, token_ticker, action=None):
    if action.lower() == "buy":
        return await buy(client, bot_username, contract_address, token_ticker)
    elif action.lower() == "sell":
        return await sell(client, bot_username, contract_address, token_ticker)
    else:
        raise ValueError("Invalid action specified. Use 'buy' or 'sell'.")

async def buy(client, bot_username, contract_address):
    print(f"Sending /start command to {bot_username}...")
    await client.send_message(bot_username, '/start')

    sol_balance = 0.0
    is_success = False

    async def handle_bot_response(event, event_type=None):
        nonlocal sol_balance
        message_text = event.message.message
        print(f"{event_type} from {bot_username}: {message_text}, message id: {event.message.id}")
        print("-------------------------------------\n\n")

        try:
            if event_type == "new_message" and "Balance:" in message_text:
                sol_balance = extract_sol_balance(message_text)
                print(f"Extracted SOL Balance: {sol_balance}")

            if event.message.buttons:
                for row in event.message.buttons:
                    for button in row:
                        print(f"{button.text} | ")
                        if button.text.lower() == "buy":
                            await button.click()
                            return

            if "enter a token symbol or address to buy" in message_text.lower():
                print(f"Sending contract address: {contract_address}\n\n")
                await client.send_message(bot_username, contract_address)
                return

            if "\ud83d\udd34" in message_text:  # Unicode for the red circle emoji (🔴)
                # Add a failed trade logic here and log it
                return

            if "\ud83d\udfe2" in message_text:  # Unicode for the green circle emoji (🟢)
                print(f"Trade executed!")
                is_success = True
                print(message_text)
                # Add a successful trade logic here and log it
                return

        except Exception as e:
            print(f"Error processing bot response: {e}")

    @client.on(events.NewMessage(chats=bot_username))
    async def handle_new_message(event, event_type="new_message"):
        await handle_bot_response(event, event_type)

    @client.on(events.MessageEdited(chats=bot_username))
    async def handle_edited_message(event, event_type="edited_message"):
        await handle_bot_response(event, event_type)

    await client.run_until_disconnected()
    return is_success

async def sell(client, bot_username, contract_address, amt=None):
    """
    Sell function for automating trades. 
    TODO: Implement the sell logic similar to the buy logic.
    """
    print(f"Sell functionality is not yet implemented. Placeholder for future logic.")
    return False, 0.0, 0.0

def extract_sol_balance(message_text):
    try:
        match = re.search(r"Balance:\s([\d.]+)\sSOL", message_text)
        if match:
            return float(match.group(1))
    except Exception as e:
        print(f"Error extracting SOL balance: {e}")
    return 0.0

def extract_trade_amount(message_text):
    try:
        match = re.search(r"Amount:\s([\d.]+)", message_text)
        if match:
            return float(match.group(1))
    except Exception as e:
        print(f"Error extracting trade amount: {e}")
    return 0.0

def extract_trade_price(message_text):
    try:
        match = re.search(r"Price:\s([\d.]+)", message_text)
        if match:
            return float(match.group(1))
    except Exception as e:
        print(f"Error extracting trade price: {e}")
    return 0.0
