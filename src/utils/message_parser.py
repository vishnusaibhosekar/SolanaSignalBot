def extract_token_data(message_text):
    """
    Extracts the contract address and token ticker from the provided message.

    Args:
        message_text (str): The text of the message to parse.

    Returns:
        tuple: The extracted contract address and token ticker, or an error message if parsing fails.
    """
    lines = message_text.split("\n")
    ca = None
    token_ticker = None

    for line in lines:
        if "💊" in line:
            token_ticker = extract_text_between_markers(line)
        if line.startswith("`"):
            ca = line[1:-1]

    if ca is not None and token_ticker is not None:
        return ca, token_ticker

    return "Error with CA parser", "Error with token ticker parser"

def extract_text_between_markers(message_text):
    """
    Extracts text between the markers "]** **" and the next occurrence of "**".

    Args:
        message_text (str): The text of the message to parse.

    Returns:
        str: The extracted text or None if not found.
    """
    start_marker = "]** **"
    end_marker = "**"

    start_index = message_text.find(start_marker)
    if start_index != -1:
        start_index += len(start_marker)
        end_index = message_text.find(end_marker, start_index)
        if end_index != -1:
            return message_text[start_index:end_index].strip()

    return None
