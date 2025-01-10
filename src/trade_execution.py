from telethon import events
import re

async def automate_solana_trojan_bot(client, bot_username, contract_address, amt=None):
    print(f"Sending /start command to {bot_username}...")
    await client.send_message(bot_username, '/start')

    sol_balance = 0.0
    trade_amount = 0.0
    trade_price = 0.0

    @client.on(events.NewMessage(chats=bot_username))
    async def handle_bot_response(event):
        nonlocal sol_balance, trade_amount, trade_price
        message_text = event.message.message
        print(f"New message from {bot_username}: {message_text}")

        try:
            if "Balance:" in message_text and sol_balance == 0.0:
                sol_balance = extract_sol_balance(message_text)
                print(f"Extracted SOL Balance: {sol_balance}")

            if event.message.buttons:
                for row in event.message.buttons:
                    for button in row:
                        print(f"Button Text: {button.text}")
                        if "SOL ✏️" in button.text:
                            print("Clicking the 'SOL ✏️' button...")
                            await button.click()
                            return
                        if button.text.lower() == "buy":
                            print("Clicking the 'Buy' button...")
                            await button.click()
                            return

            if "enter a token symbol or address to buy" in message_text.lower():
                print(f"Sending contract address: {contract_address}")
                await client.send_message(bot_username, contract_address)
                return

            if "enter sol amount" in message_text.lower():
                if amt is None:
                    amt = round(sol_balance * 0.01, 4)
                print(f"Sending amount: {amt}")
                await client.send_message(bot_username, str(amt))
                return

            if "Trade executed" in message_text:
                trade_amount = extract_trade_amount(message_text)
                trade_price = extract_trade_price(message_text)
                print(f"Trade executed: Amount={trade_amount}, Price={trade_price}")
                return

        except Exception as e:
            print(f"Error processing bot response: {e}")

    await client.run_until_disconnected()
    return trade_amount > 0, trade_amount, trade_price

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
