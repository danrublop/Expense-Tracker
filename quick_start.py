#!/usr/bin/env python3
"""
Quick Start Script for Telegram Expense Logging Bot
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_setup():
    """Check the current setup status."""
    print("🔍 Checking your setup...")
    print()
    
    # Check .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Run: python3 setup.py")
        return False
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    required_vars = {
        'TELEGRAM_BOT_TOKEN': 'Bot token from @BotFather',
        'SPREADSHEET_ID': 'Google Sheets ID',
        'WEBAPP_URL': 'Google Apps Script Web App URL'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_vars.append(f"  • {var}: {description}")
        else:
            print(f"✅ {var}: {value[:50]}{'...' if len(value) > 50 else ''}")
    
    if missing_vars:
        print("\n❌ Missing environment variables:")
        for var in missing_vars:
            print(var)
        print("\n💡 Run: python3 setup_google_sheets.py")
        return False
    
    print("\n✅ All environment variables are set!")
    return True

def test_connection():
    """Test the Google Sheets connection."""
    print("\n🧪 Testing Google Sheets connection...")
    
    try:
        from sheets.operations import SheetOperations
        sheet_ops = SheetOperations()
        
        if sheet_ops.is_connected():
            print("✅ Google Sheets connection successful!")
            conn_info = sheet_ops.get_connection_info()
            print(f"📊 Spreadsheet ID: {conn_info['spreadsheet_id']}")
            print(f"🔗 Web App URL: {conn_info['webapp_url']}")
            return True
        else:
            print("❌ Google Sheets connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {str(e)}")
        return False

def run_tests():
    """Run the test suite."""
    print("\n🧪 Running test suite...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_bot.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {str(e)}")
        return False

def start_bot():
    """Start the bot."""
    print("\n🚀 Starting the bot...")
    print("   Press Ctrl+C to stop the bot")
    print()
    
    try:
        import subprocess
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n✅ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {str(e)}")

def main():
    """Main quick start function."""
    print("=" * 60)
    print("🚀 Quick Start - Telegram Expense Logging Bot")
    print("=" * 60)
    print()
    
    # Check setup
    if not check_setup():
        return
    
    # Test connection
    if not test_connection():
        print("\n💡 Your Google Sheets setup may need attention.")
        print("   Run: python3 setup_google_sheets.py")
        return
    
    # Run tests
    if not run_tests():
        print("\n💡 Tests failed. Check the errors above.")
        return
    
    # All good! Ask if user wants to start the bot
    print("\n🎉 Everything is working! Your bot is ready to go.")
    print()
    
    response = input("Would you like to start the bot now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        start_bot()
    else:
        print("\n📚 To start your bot later, run:")
        print("   python3 main.py")
        print("\n💡 To test your bot:")
        print("   1. Find your bot on Telegram")
        print("   2. Send /start")
        print("   3. Try logging an expense: '6.60 food'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Quick start failed: {str(e)}")
        sys.exit(1)
