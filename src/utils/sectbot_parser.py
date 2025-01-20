def sectbot_parse_message(message_text):
    """
    Extracts structured data from SectBot messages using string manipulation.

    Args:
        message_text (str): The text of the message to parse.

    Returns:
        dict: A dictionary containing the extracted data.
    """
    data = {}

    # Split the message into lines for easier processing
    lines = message_text.split("\n")

    # Extract contract address (look for the line with ├)
    data["contract_address"] = None
    for line in lines:
        if "├" in line:
            parts = line.split("├")
            if len(parts) > 1:
                data["contract_address"] = parts[1].strip()
                break

    # Extract token ticker (look for the "Call" line)
    data["token_ticker"] = None
    for line in lines:
        if "Call" in line and "$" in line:
            data["token_ticker"] = line.split("(")[1].split(")")[0].strip()
            break

    # Extract chain (look for the "🟣" line)
    data["chain"] = None
    for line in lines:
        if "🟣" in line:
            parts = line.split("🟣")
            if len(parts) > 1:
                data["chain"] = parts[1].split("|")[0].strip()
            break

    # Extract Market Cap (MC) and Volume (Vol) (look for the line with "MC")
    data["market_cap"] = None
    data["volume"] = None
    for line in lines:
        if "MC" in line and "Vol" in line:
            try:
                parts = line.split("|")
                for part in parts:
                    if "MC" in part:
                        data["market_cap"] = part.split(":")[1].strip()
                    if "Vol" in part:
                        data["volume"] = part.split(":")[1].strip()
            except IndexError:
                pass
            break

    # Extract Dex Screener link (look for "DXSCR")
    data["dex_screener_link"] = None
    for line in lines:
        if "DXSCR" in line:
            try:
                parts = line.split("|")
                for part in parts:
                    if "DXSCR" in part:
                        link_start = part.find("(") + 1
                        link_end = part.find(")")
                        data["dex_screener_link"] = part[link_start:link_end].strip()
                        break
            except IndexError:
                pass
            break

    # Extract caller name and action (look for the "Called by" line)
    data["caller_name"] = None
    data["caller_action"] = None
    for line in lines:
        if "Called by" in line:
            try:
                # Extract the caller's name (starts after "@")
                start_index = line.index("@") + 1
                data["caller_name"] = line[start_index:].split(" ")[0].strip()
                # Extract the caller's action (within parentheses)
                action_start = line.index("(") + 1
                action_end = line.index(")")
                data["caller_action"] = line[action_start:action_end].strip()
            except (IndexError, ValueError):
                pass
            break

    # Extract win rate (look for "Win Rate")
    data["win_rate"] = None
    for line in lines:
        if "Win Rate" in line:
            try:
                data["win_rate"] = line.split("Win Rate:")[1].split("%")[0].strip() + "%"
            except IndexError:
                pass
            break

    # Extract number of calls (look for "Nº Calls")
    data["num_calls"] = None
    for line in lines:
        if "Nº Calls" in line:
            try:
                # Extract everything after "Nº Calls:" and strip it
                data["num_calls"] = line.split("Nº Calls:")[1].strip()
            except IndexError:
                pass
            break

    return data

if __name__ == "__main__":
    # Example message to parse
    message_text = """"✅ Call for TxNarrator ($TxNarrator)
                        ├EcTgyj6owNLinBYHqWiWbQMLhQbSpthWy8YZDBSipump
                        🟣SOL|MC:$69.4K|Vol:$582.0K

                        🖥 Stats (https://sectbot.com/tokens/solana/EcTgyj6owNLinBYHqWiWbQMLhQbSpthWy8YZDBSipump)|21 calls|First:41.5K MC
                        🌐 Web (https://www.txnarrator.com/) | TG (https://t.me/txnarrator_community) | X (https://x.com/TxNarrator)
                        📊 DXV (https://www.dexview.com/solana/EcTgyj6owNLinBYHqWiWbQMLhQbSpthWy8YZDBSipump) | DXT (https://www.dextools.io/app/en/solana/pair-explorer/2z91wYpBZ2sop1G1HMMihxEcmzyaQ5NrS51MVtXpVH1n) | DXSCR (https://dexscreener.com/solana/2z91wypbz2sop1g1hmmihxecmzyaq5nrs51mvtxpvh1n) | MevX (https://mevx.io/solana/EcTgyj6owNLinBYHqWiWbQMLhQbSpthWy8YZDBSipump?ref=sectbot) | Photon (https://photon-sol.tinyastro.io/en/r/@EMILIAN/EcTgyj6owNLinBYHqWiWbQMLhQbSpthWy8YZDBSipump)
                        💰 Buy: MAESTRO (https://t.me/maestro?start=2z91wYpBZ2sop1G1HMMihxEcmzyaQ5NrS51MVtXpVH1n-sect) | SHUR (https://t.me/ShurikenTradeBot?start=qt-sect-2z91wYpBZ2sop1G1HMMihxEcmzyaQ5NrS51MVtXpVH1n)
                        └ 🫧 BMap (https://t.me/pirbviewbot?start=EcTgyj6owNLinBYHqWiWbQMLhQbSpthWy8YZDBSipump--b) | 🐋 WMap (https://t.me/pirbviewbot?start=EcTgyj6owNLinBYHqWiWbQMLhQbSpthWy8YZDBSipump--w) | 🫂 TH (https://t.me/pirbviewbot?start=EcTgyj6owNLinBYHqWiWbQMLhQbSpthWy8YZDBSipump--h)

                        👤Called by @satyaj2 (🎲 Gamble)
                        ├ Win Rate: 66.70% 🟡
                        ├ Nº Calls: 3
                        └ Sect Bot Profile (https://sectbot.com/caller/satyaj2)"""
    
    # Parse the message
    parsed_data = parse_message(message_text)
    
    # Print the extracted data
    for key, value in parsed_data.items():
        print(f"{key}: {value}")
