"""
Utility functions for the Telegram Expense Logging Bot.
"""
import re
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

def parse_expense_message(message: str) -> Tuple[Optional[float], Optional[str], str]:
    """
    Parse an expense message to extract amount and category.
    
    Args:
        message: The message text to parse
        
    Returns:
        Tuple of (amount, category, error_message)
    """
    try:
        # Remove extra whitespace and convert to lowercase for parsing
        message = message.strip()
        
        if not message:
            return None, None, "❌ Message is empty."
        
        # Pattern to match: amount (with optional decimal) followed by description
        # Supports: 6.60, 6,60, 6, 6.0, etc.
        pattern = r'^(\d+(?:[.,]\d+)?)\s+(.+)$'
        match = re.match(pattern, message)
        
        if not match:
            return None, None, "❌ Invalid format. Please use: `amount category` (e.g., `6.60 food`)"
        
        amount_str, category = match.groups()
        
        # Convert amount string to float
        # Handle both comma and dot as decimal separators
        amount_str = amount_str.replace(',', '.')
        
        try:
            amount = float(amount_str)
        except ValueError:
            return None, None, "❌ Invalid amount. Please enter a valid number."
        
        # Validate amount
        if amount <= 0:
            return None, None, "❌ Amount must be greater than 0."
        
        if amount > 1000000:  # $1M limit
            return None, None, "❌ Amount seems too high. Please check and try again."
        
        # Clean up category
        category = category.strip()
        
        if not category:
            return None, None, "❌ Please provide a description for your expense."
        
        if len(category) > 100:
            return None, None, "❌ Description is too long. Please keep it under 100 characters."
        
        logger.info(f"Successfully parsed expense: ${amount} for {category}")
        return amount, category, ""
        
    except Exception as e:
        logger.error(f"Error parsing expense message '{message}': {str(e)}")
        return None, None, f"❌ Error parsing message: {str(e)}"

def validate_amount(amount: float) -> Tuple[bool, str]:
    """
    Validate an expense amount.
    
    Args:
        amount: The amount to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(amount, (int, float)):
        return False, "❌ Amount must be a number."
    
    if amount <= 0:
        return False, "❌ Amount must be greater than 0."
    
    if amount > 1000000:  # $1M limit
        return False, "❌ Amount seems too high. Please check and try again."
    
    # Check for reasonable precision (max 2 decimal places)
    if round(amount, 2) != amount:
        return False, "❌ Amount can have maximum 2 decimal places."
    
    return True, ""

def validate_category(category: str) -> Tuple[bool, str]:
    """
    Validate an expense category/description.
    
    Args:
        category: The category to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(category, str):
        return False, "❌ Category must be text."
    
    if not category or not category.strip():
        return False, "❌ Please provide a description for your expense."
    
    if len(category.strip()) > 100:
        return False, "❌ Description is too long. Please keep it under 100 characters."
    
    # Check for potentially harmful content
    harmful_patterns = [
        r'<script', r'javascript:', r'data:', r'vbscript:', r'onload=',
        r'onerror=', r'onclick=', r'<iframe', r'<object', r'<embed'
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, category, re.IGNORECASE):
            return False, "❌ Description contains invalid content."
    
    return True, ""

def format_currency(amount: float) -> str:
    """
    Format an amount as currency.
    
    Args:
        amount: The amount to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:.2f}"

def sanitize_text(text: str) -> str:
    """
    Sanitize text input to prevent injection attacks.
    
    Args:
        text: The text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove or escape potentially harmful characters
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('&', '&amp;').replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    
    # Remove newlines and excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_command_args(message: str) -> Tuple[str, str]:
    """
    Extract command and arguments from a message.
    
    Args:
        message: The message text
        
    Returns:
        Tuple of (command, arguments)
    """
    message = message.strip()
    
    if not message.startswith('/'):
        return "", message
    
    # Split on first space
    parts = message.split(' ', 1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    
    return command, args

def is_command(message: str) -> bool:
    """
    Check if a message is a command.
    
    Args:
        message: The message text
        
    Returns:
        True if the message is a command
    """
    return message.strip().startswith('/')

def get_suggested_categories() -> list:
    """
    Get a list of suggested expense categories.
    
    Returns:
        List of suggested categories
    """
    return [
        'food', 'coffee', 'groceries', 'gas', 'transport', 'entertainment',
        'shopping', 'utilities', 'rent', 'insurance', 'health', 'other'
    ]

def format_category_suggestions() -> str:
    """
    Format category suggestions for display.
    
    Returns:
        Formatted string with category suggestions
    """
    categories = get_suggested_categories()
    return "💡 **Suggested categories:** " + ", ".join(categories)
