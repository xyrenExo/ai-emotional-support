import bleach
import re
from app.config import Config

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS and injection attacks"""
    # Remove any HTML/script tags
    cleaned = bleach.clean(text, strip=True)
    
    # Remove any potential injection patterns
    cleaned = re.sub(r'[<>{}]', '', cleaned)
    
    # Limit length
    cleaned = cleaned[:Config.MAX_MESSAGE_LENGTH]
    
    return cleaned

def validate_message(message: str) -> bool:
    """Validate message content"""
    if not message or not isinstance(message, str):
        return False
    
    if len(message.strip()) == 0:
        return False
    
    if len(message) > Config.MAX_MESSAGE_LENGTH:
        return False
    
    return True