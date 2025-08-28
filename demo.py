#!/usr/bin/env python3
"""
Demo script for the Telegram Expense Logging Bot.
This script demonstrates the bot's functionality without requiring Telegram or Google Sheets.
"""
import sys
from datetime import datetime
from bot.utils import parse_expense_message, format_currency, get_suggested_categories

def print_banner():
    """Print the demo banner."""
    print("=" * 60)
    print("🤖 Telegram Expense Logging Bot - Demo")
    print("=" * 60)
    print()

def demo_message_parsing():
    """Demonstrate message parsing functionality."""
    print("📝 **Message Parsing Demo**")
    print("The bot can parse expense messages in various formats:\n")
    
    demo_messages = [
        "6.60 food",
        "9.70 coffee at starbucks",
        "15.30 groceries",
        "125.00 gas",
        "6,60 food",  # Comma decimal
        "6 food",     # Integer amount
        "0.50 snack", # Small amount
    ]
    
    for message in demo_messages:
        amount, category, error_msg = parse_expense_message(message)
        if amount and category:
            print(f"✅ '{message}' → {format_currency(amount)} for {category}")
        else:
            print(f"❌ '{message}' → {error_msg}")
    
    print("\n" + "-" * 40)

def demo_validation():
    """Demonstrate input validation."""
    print("🔍 **Input Validation Demo**")
    print("The bot validates all inputs for security and accuracy:\n")
    
    # Test invalid inputs
    invalid_inputs = [
        "food",           # No amount
        "6.60",          # No category
        "abc food",      # Invalid amount
        "-5.00 food",    # Negative amount
        "1000001.00 rent", # Too high amount
    ]
    
    for message in invalid_inputs:
        amount, category, error_msg = parse_expense_message(message)
        print(f"❌ '{message}' → {error_msg}")
    
    print("\n" + "-" * 40)

def demo_commands():
    """Demonstrate available commands."""
    print("⌨️  **Available Commands**")
    print("Users can interact with the bot using these commands:\n")
    
    commands = [
        ("/start", "Welcome message and usage instructions"),
        ("/help", "Show command formats and examples"),
        ("/total", "Show total expenses"),
        ("/stats", "Show spending statistics"),
        ("/stats 2024-08", "Show stats for specific month"),
        ("/recent", "Show recent expenses (default: 5)"),
        ("/recent 10", "Show 10 most recent expenses"),
    ]
    
    for command, description in commands:
        print(f"• {command:<15} - {description}")
    
    print("\n" + "-" * 40)

def demo_google_sheets_integration():
    """Demonstrate Google Sheets integration."""
    print("📊 **Google Sheets Integration Demo**")
    print("The bot uses a single worksheet for all expenses:\n")
    
    print("📋 Worksheet: Expenses")
    print("📋 Sheet structure:")
    print("   A: Date | B: Time | C: Amount | D: Category | E: Running Total")
    print("\n📝 Example data:")
    print("   2024-08-15 | 14:30 | $6.60 | food | $6.60")
    print("   2024-08-15 | 16:45 | $9.70 | coffee | $16.30")
    print("   2024-08-15 | 19:20 | $15.30 | groceries | $31.60")
    print("   2024-08-16 | 12:00 | $25.00 | lunch | $56.60")
    
    print("\n" + "-" * 40)

def demo_user_experience():
    """Demonstrate the user experience."""
    print("👤 **User Experience Demo**")
    print("Here's how a typical conversation would look:\n")
    
    print("🤖 Bot: Welcome! Send me expenses like '6.60 food'")
    print("👤 User: 6.60 food")
    print("🤖 Bot: ✅ Logged $6.60 for food. Running total: $6.60")
    print("🤖 Bot: 💡 Suggested categories: food, coffee, groceries, gas...")
    print()
    print("👤 User: /total")
    print("🤖 Bot: 💰 Total expenses: $6.60")
    print()
    print("👤 User: 9.70 coffee at starbucks")
    print("🤖 Bot: ✅ Logged $9.70 for coffee at starbucks. Running total: $16.30")
    
    print("\n" + "-" * 40)

def demo_features():
    """Demonstrate advanced features."""
    print("🚀 **Advanced Features**")
    print("The bot includes several advanced capabilities:\n")
    
    features = [
        "🔒 Input validation and sanitization",
        "📊 Automatic running total calculation",
        "📅 Single worksheet for all expenses",
        "💡 Category suggestions and auto-completion",
        "📈 Spending statistics and breakdowns",
        "📈 Monthly filtering with /stats 2024-08",
        "🔍 Recent expense tracking",
        "⚡ Rate limiting and error handling",
        "📝 Comprehensive logging and monitoring",
    ]
    
    for feature in features:
        print(f"• {feature}")
    
    print("\n" + "-" * 40)

def demo_setup():
    """Demonstrate the setup process."""
    print("⚙️  **Setup Process**")
    print("Getting started is easy with our automated setup:\n")
    
    setup_steps = [
        "1. Run 'python setup.py'",
        "2. Enter your Telegram bot token",
        "3. Provide Google credentials file path",
        "4. Enter your Google spreadsheet ID",
        "5. Run 'python test_bot.py' to verify",
        "6. Start the bot with 'python main.py'",
    ]
    
    for step in setup_steps:
        print(f"   {step}")
    
    print("\n" + "-" * 40)

def main():
    """Run the demo."""
    print_banner()
    
    print("This demo showcases the Telegram Expense Logging Bot's capabilities")
    print("without requiring actual Telegram or Google Sheets setup.\n")
    
    demos = [
        ("Message Parsing", demo_message_parsing),
        ("Input Validation", demo_validation),
        ("Available Commands", demo_commands),
        ("Google Sheets Integration", demo_google_sheets_integration),
        ("User Experience", demo_user_experience),
        ("Advanced Features", demo_features),
        ("Setup Process", demo_setup),
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
            print()
        except Exception as e:
            print(f"❌ Error in {demo_name} demo: {str(e)}")
            print()
    
    print("=" * 60)
    print("🎉 Demo completed!")
    print("=" * 60)
    print("\nTo get started with your own bot:")
    print("1. Follow the setup guide in SETUP_GUIDE.md")
    print("2. Run 'python setup.py' to configure")
    print("3. Test with 'python test_bot.py'")
    print("4. Start with 'python main.py'")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during demo: {str(e)}")
        sys.exit(1)
