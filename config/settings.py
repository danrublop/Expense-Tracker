"""
Configuration settings for the Telegram Expense Logging Bot.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

# Google Sheets Configuration
GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'config/credentials.json')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
if not SPREADSHEET_ID:
    raise ValueError("SPREADSHEET_ID environment variable is required")

WEBAPP_URL = os.getenv('WEBAPP_URL')
if not WEBAPP_URL:
    raise ValueError("WEBAPP_URL environment variable is required")

# Bot Settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
RATE_LIMIT_DELAY = float(os.getenv('RATE_LIMIT_DELAY', '1.0'))

# Google Sheets Configuration
SHEET_HEADERS = ['Date', 'Time', 'Amount', 'Category', 'Running Total']
DEFAULT_CATEGORIES = [
    'food', 'coffee', 'groceries', 'gas', 'transport', 'entertainment',
    'shopping', 'utilities', 'rent', 'insurance', 'health', 'other'
]

# Message Templates
WELCOME_MESSAGE = """
🤖 Welcome to the Expense Logging Bot!

📝 **How to use:**
Simply send me a message in this format:
• `6.60 food`
• `9.70 coffee at starbucks`
• `15.30 groceries`
• `125.00 gas`

💡 **Available commands:**
/start - Show this message
/help - Show usage examples
/total - Show total expenses
/stats - Show spending statistics
/recent - Show recent expenses
/monthly_report - Monthly report with options
/annual_report - Annual report with options
/analyze_monthly - AI-powered monthly analysis
/analyze_annual - AI-powered annual analysis

💰 I'll automatically log your expenses to Google Sheets and track your total spending!
🤖 **NEW**: Advanced AI analysis using local Mistral LLM!
📊 **NEW**: Interactive report buttons for easy access!
"""

HELP_MESSAGE = """
📚 **Usage Examples:**

**Basic format:** `amount category`
• `6.60 food`
• `9.70 coffee`
• `15.30 groceries`

**With description:** `amount description`
• `9.70 coffee at starbucks`
• `25.50 lunch with colleagues`
• `45.00 movie tickets`

**Commands:**
• `/total` - Show total expenses
• `/stats` - Show spending statistics
• `/stats 2024-08` - Show stats for specific month
• `/recent` - Show recent expenses
• `/monthly_report` - Monthly report with button options
• `/annual_report` - Annual report with button options
• `/analyze_monthly` - AI-powered monthly analysis
• `/analyze_annual` - AI-powered annual analysis
• `/help` - Show this help message

🤖 **AI Analysis Features:**
• **Flow-based processing**: Data is analyzed in stages for better accuracy
• **Smart categorization**: Automatically groups similar expenses
• **Pattern recognition**: Identifies recurring spending (e.g., "matcha 20 times")
• **Local privacy**: Uses local Mistral LLM via Ollama
• **Insights & recommendations**: Provides actionable financial advice

💡 **Tips:**
• Amounts can use dots or commas: 6.60 or 6,60
• Categories are case-insensitive
• All expenses are logged to one sheet
• Running totals are calculated automatically
• AI analysis requires Ollama to be running locally
"""

ERROR_INVALID_FORMAT = "❌ Invalid format. Please use: `amount category` (e.g., `6.60 food`)"
ERROR_INVALID_AMOUNT = "❌ Invalid amount. Please enter a valid number."
ERROR_MISSING_DESCRIPTION = "❌ Please provide a description for your expense."
ERROR_SHEETS_API = "❌ Error connecting to Google Sheets. Please try again later."
SUCCESS_MESSAGE = "✅ Logged ${amount} for {category}. Running total: ${running_total}"

# Date and Time Formats
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
