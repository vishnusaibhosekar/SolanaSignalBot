def parse_message(message_text):
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

    # Extract contract address (look for the line with backticks or pipe)
    data["contract_address"] = None
    for line in lines:
        if "`" in line or "|" in line:
            parts = line.split("`")
            if len(parts) > 1:
                data["contract_address"] = parts[1].strip()
                break

    # Extract token ticker (look for the "Call" line)
    data["token_ticker"] = None
    for line in lines:
        if "Call" in line:
            try:
                data["token_ticker"] = line.split("(")[1].split(")")[0].strip()
            except IndexError:
                pass
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
                        # Remove '**' and clean the value
                        data["market_cap"] = part.split(":")[1].replace("**", "").strip()
                    if "Vol" in part:
                        # Remove '**' and clean the value
                        data["volume"] = part.split(":")[1].replace("**", "").strip()
            except IndexError:
                pass
            break
        
    # Extract Dex Screener link (look for "DXSCR")
    data["dex_screener_link"] = None
    for line in lines:
        if "DXSCR" in line:
            try:
                # Split the line into parts and find the one containing "DXSCR"
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
                parts = line.split(" ")
                data["caller_name"] = parts[2].lstrip("@")
                data["caller_action"] = parts[3].strip("()")
            except IndexError:
                pass
            break

    # Extract win rate (look for the "Win Rate" line)
    data["win_rate"] = None
    for line in lines:
        if "Win Rate" in line:
            try:
                data["win_rate"] = line.split("**")[1].strip()
            except IndexError:
                pass
            break

    # Extract number of calls (look for the "Nº Calls" line)
    data["num_calls"] = None
    for line in lines:
        if "Nº Calls" in line:
            try:
                data["num_calls"] = line.split("**")[1].strip()
            except IndexError:
                pass
            break

    return data
