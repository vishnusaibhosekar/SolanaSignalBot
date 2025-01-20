from telethon import events
import re

# Track if event listeners have been registered
event_listeners_registered = False
current_trade = {"in_progress": False, "contract_address": None, "action": None}  # Track trade state

async def automate_solana_trojan_bot(client, bot_username, contract_address, token_ticker, action=None):
    print(f"automate_solana_trojan_bot called: {client, bot_username, contract_address, token_ticker, action}" )
    return
    global event_listeners_registered

    if not event_listeners_registered:
        register_event_listeners(client, bot_username, contract_address, token_ticker, action)
        event_listeners_registered = True

    if action.lower() == "buy":
        return await execute_trade(client, bot_username, contract_address, token_ticker, "buy")
    elif action.lower() == "sell":
        return await execute_trade(client, bot_username, contract_address, token_ticker, "sell")
    else:
        raise ValueError("Invalid action specified. Use 'buy' or 'sell'.")

def register_event_listeners(client, bot_username, contract_address, token_ticker, action):
    """Register event listeners for new and edited messages."""
    @client.on(events.NewMessage(chats=bot_username))
    async def handle_new_message(event):
        await handle_bot_response(event, "new_message", client, bot_username, contract_address, token_ticker, action)

    @client.on(events.MessageEdited(chats=bot_username))
    async def handle_edited_message(event):
        await handle_bot_response(event, "edited_message", client, bot_username, contract_address, token_ticker, action)

async def handle_bot_response(event, event_type, client, bot_username, contract_address, token_ticker, action):
    global current_trade

    message_text = event.message.message
    # print("\n-------------------------------------\n")
    # print(f"message id: {event.message.id} - {event_type} from bot: {message_text}")
    # print("\n-------------------------------------\n")
    
    try:
        # If a trade is already in progress, process only relevant follow-up messages
        if current_trade["in_progress"]:
            if "Buy Success" in message_text or "Sell Success" in message_text:
                print("Trade executed successfully!")
                current_trade = {"in_progress": False, "contract_address": None, "action": None}
            return

        # Process trade initiation
        if "Balance:" in message_text and event_type == "new_message":
            sol_balance = extract_sol_balance(message_text)
            print(f"Extracted SOL Balance: {sol_balance}\n")

        if event.message.buttons:
            for row in event.message.buttons:
                print("*************************************")
                print(" | ".join(button.text for button in row))
                print("*************************************")
                for button in row:
                    if button.text.lower() == current_trade.get("action", ""):
                        print(f"Button clicked: {button.text}")
                        await button.click()
                        return

        if "enter a token symbol or address" in message_text.lower():
            print(f"Sending contract address: {contract_address}\n")
            await client.send_message(bot_username, contract_address)
            current_trade["in_progress"] = True
            return

    except Exception as e:
        print(f"Error processing bot response: {e}")
        current_trade = {"in_progress": False, "contract_address": None, "action": None}

async def execute_trade(client, bot_username, contract_address, token_ticker, action):
    global current_trade
    print(f"\nSending /start command to {bot_username}...\n")
    current_trade.update({"in_progress": False, "contract_address": contract_address, "action": action})
    await client.send_message(bot_username, '/start')

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
