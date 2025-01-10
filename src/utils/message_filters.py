def sender_filter(sender_id, allowed_senders):
    """
    Filters messages based on sender IDs.
    
    Args:
        sender_id (int): The ID of the message sender.
        allowed_senders (list): List of allowed sender IDs.
    
    Returns:
        bool: True if the sender is allowed, False otherwise.
    """
    return sender_id in allowed_senders


def keyword_filter(message_text, allowed_keywords):
    """
    Filters messages based on keywords.
    
    Args:
        message_text (str): The text of the message.
        allowed_keywords (list): List of allowed keywords.
    
    Returns:
        bool: True if the message contains any of the allowed keywords, False otherwise.
    """
    return all(keyword.lower() in message_text.lower() for keyword in allowed_keywords)


def apply_filters(sender_id, message_text):
    """
    Combines all filters: sender ID and keywords.
    
    Args:
        sender_id (int): The ID of the message sender.
        message_text (str): The text of the message.
    
    Returns:
        bool: True if the message passes all filters, False otherwise.
    """
    # List of allowed sender IDs (update with real IDs)
    allowed_senders = [5484082105]  # Replace with real sender IDs

    # Combine sender filter and keyword filter
    return sender_filter(sender_id, allowed_senders)
