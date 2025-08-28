#!/usr/bin/env python3
"""
Setup script for the Telegram Expense Logging Bot.
"""
import os
import sys
import json
from pathlib import Path

def print_banner():
    """Print the setup banner."""
    print("=" * 60)
    print("🤖 Telegram Expense Logging Bot - Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def create_directories():
    """Create necessary directories."""
    directories = ['config', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Created necessary directories")

def create_env_file():
    """Create .env file from template."""
    env_file = Path('.env')
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return
    
    print("\n📝 Creating .env file...")
    print("Please provide the following information:")
    
    bot_token = input("Telegram Bot Token: ").strip()
    if not bot_token:
        print("❌ Bot token is required!")
        sys.exit(1)
    
    spreadsheet_id = input("Google Spreadsheet ID: ").strip()
    if not spreadsheet_id:
        print("❌ Spreadsheet ID is required!")
        sys.exit(1)
    
    webapp_url = input("Google Apps Script Web App URL: ").strip()
    if not webapp_url:
        print("❌ Web App URL is required!")
        sys.exit(1)
    
    # Create .env file
    env_content = f"""# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={bot_token}

# Google Sheets Configuration (Apps Script)
SPREADSHEET_ID={spreadsheet_id}
WEBAPP_URL={webapp_url}

# Bot Settings
LOG_LEVEL=INFO
MAX_RETRIES=3
RATE_LIMIT_DELAY=1.0
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file")

def print_setup_instructions():
    """Print setup instructions for Google Apps Script."""
    print("\n📋 **Google Apps Script Setup Required**")
    print("Before running the bot, you need to:")
    print("1. Create a Google Sheet")
    print("2. Add the Apps Script (see SETUP_GUIDE.md)")
    print("3. Deploy as Web App")
    print("4. Get the Web App URL")
    print("\n📚 See SETUP_GUIDE.md for detailed instructions")

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    try:
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        print("✅ Dependencies installed successfully")
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Please run: pip install -r requirements.txt")

def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Complete Google Apps Script setup (see SETUP_GUIDE.md)")
    print("2. Test the bot by running: python main.py")
    print("3. Send /start to your bot on Telegram")
    print("\n📚 For more information, see SETUP_GUIDE.md")
    print("\n🔧 Troubleshooting:")
    print("- Check that all environment variables are set correctly")
    print("- Verify Google Apps Script is deployed and accessible")
    print("- Ensure Web App has proper permissions")

def main():
    """Main setup function."""
    print_banner()
    
    try:
        check_python_version()
        create_directories()
        create_env_file()
        
        print_setup_instructions()
        
        install_dependencies()
        print_next_steps()
            
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
