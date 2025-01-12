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

def apply_filters(sender_id, message_text):
    """
    Combines all filters: sender ID and keywords.
    
    Args:
        sender_id (int): The ID of the message sender.
        message_text (str): The text of the message.
    
    Returns:
        bool: True if the message passes all filters, False otherwise.
    """
    # List of allowed sender IDs
    allowed_senders = [6126376117]  # Replace with RickBot's ID

    # Combine sender filter and keyword filter
    return sender_filter(sender_id, allowed_senders)
