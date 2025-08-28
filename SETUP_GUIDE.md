# 🚀 Complete Setup Guide for Telegram Expense Tracker Bot

This guide will walk you through setting up your Telegram Expense Tracker Bot from scratch, including BotFather configuration, Google Sheets setup, and AI analysis features.

## 📋 Prerequisites

- Python 3.8 or higher
- A Telegram account
- A Google account with Google Sheets access
- Git (for cloning the repository)

## 🔧 Step 1: Clone and Setup Repository

```bash
# Clone the repository
git clone https://github.com/danrublop/Expense-Tracker.git
cd Expense-Tracker

# Install Python dependencies
pip install -r requirements.txt
```

## 🤖 Step 2: Configure Telegram Bot with BotFather

### 2.1 Create Your Bot

1. **Open Telegram** and search for [@BotFather](https://t.me/botfather)
2. **Send `/start`** to begin
3. **Send `/newbot`** to create a new bot
4. **Choose a name** for your bot (e.g., "My Expense Tracker")
5. **Choose a username** (must end with 'bot', e.g., "my_expense_tracker_bot")
6. **Copy the bot token** that BotFather provides

### 2.2 Configure Bot Commands

Send this to BotFather to set up your bot's command menu:

```
/setcommands
```

Then paste this list:

```
start - Start the bot and show welcome message
help - Show usage examples and tips
total - Show current total expenses
stats - Show spending statistics
recent - Show recent expenses
monthly_report - Interactive monthly report with options
annual_report - Interactive annual report with options
analyze_monthly - AI-powered monthly analysis
analyze_annual - AI-powered annual analysis
```

### 2.3 Get Your Bot Token

- **Save the bot token** - you'll need it for the `.env` file
- **Test your bot** by sending `/start` to it

## 📊 Step 3: Configure Google Sheets

### 3.1 Create Google Sheet

1. **Go to [Google Sheets](https://sheets.google.com)**
2. **Create a new spreadsheet**
3. **Copy the spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
   ```

### 3.2 Set Up Google Apps Script

1. **Open your spreadsheet**
2. **Go to Extensions → Apps Script**
3. **Replace the default code** with the content from `ai_analysis_apps_script.js`
4. **Set the spreadsheet ID** in the script:
   ```javascript
   const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE';
   ```
5. **Deploy as web app**:
   - Click **Deploy → New deployment**
   - Choose **Web app** as type
   - Set **Execute as**: Me
   - Set **Who has access**: Anyone
   - Click **Deploy**
6. **Copy the web app URL** provided

## 🔐 Step 4: Environment Configuration

### 4.1 Create Environment File

```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your credentials
nano .env
```

### 4.2 Fill in Your Credentials

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather

# Google Sheets Configuration
SPREADSHEET_ID=your_spreadsheet_id_from_google_sheets
WEBAPP_URL=your_webapp_url_from_apps_script

# Optional Settings
LOG_LEVEL=INFO
MAX_RETRIES=3
RATE_LIMIT_DELAY=1.0
```

### 4.3 Example .env File

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
SPREADSHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
WEBAPP_URL=https://script.google.com/macros/s/AKfycbx1234567890abcdef/exec
LOG_LEVEL=INFO
MAX_RETRIES=3
RATE_LIMIT_DELAY=1.0
```

## 🤖 Step 5: Set Up AI Analysis (Optional)

### 5.1 Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
- Download from [ollama.ai](https://ollama.ai)
- Or use WSL2 and follow Linux instructions

### 5.2 Download Mistral Model

```bash
# Start Ollama service
ollama serve

# In another terminal, pull the model
ollama pull mistral
```

### 5.3 Test Ollama Setup

```bash
# Test basic functionality
ollama run mistral "Hello, how are you?"

# Test with your bot
python3 test_ai_analysis.py
```

## 🧪 Step 6: Test Your Setup

### 6.1 Test Basic Functionality

```bash
# Test Google Sheets connection
python3 quick_start.py

# Test bot functionality
python3 test_bot.py

# Test button functionality
python3 test_button_functionality.py

# Test AI analysis (if Ollama is set up)
python3 test_ai_analysis.py
```

### 6.2 Test Google Apps Script

1. **Go to your Apps Script project**
2. **Run the `testAIAnalysisScript` function**
3. **Check the execution log** for any errors
4. **Verify the "AI Analysis" worksheet** was created

## 🚀 Step 7: Start Your Bot

```bash
# Start the bot
python3 main.py
```

### 7.1 Test Bot Commands

Send these to your bot:
- `/start` - Welcome message
- `/help` - Usage instructions
- `6.60 coffee` - Log an expense
- `/monthly_report` - Test interactive reports
- `/analyze_monthly` - Test AI analysis

## 🔍 Troubleshooting

### Common Issues

1. **"Bot not responding"**
   - Check your bot token in `.env`
   - Ensure bot is running: `python3 main.py`
   - Verify bot is not blocked by users

2. **"Google Sheets connection failed"**
   - Run `python3 setup_google_sheets.py`
   - Verify Apps Script deployment
   - Check Web App URL in `.env`

3. **"AI Analysis not working"**
   - Ensure Ollama is running: `ollama serve`
   - Check Mistral model: `ollama list`
   - Pull model if missing: `ollama pull mistral`

4. **"Apps Script error"**
   - Ensure spreadsheet has "Expenses" worksheet
   - Check Apps Script code is correct
   - Verify deployment settings

### Getting Help

1. **Check logs**: Look at `bot.log` for detailed error messages
2. **Run tests**: Use the test scripts to identify issues
3. **Verify setup**: `python3 quick_start.py` to check configuration
4. **Check Google Apps Script**: Look for errors in the Apps Script console

## 📚 Advanced Configuration

### Custom Categories

Edit `config/settings.py` to modify default categories:
```python
DEFAULT_CATEGORIES = [
    'food', 'coffee', 'groceries', 'gas', 'transport', 
    'entertainment', 'shopping', 'utilities', 'rent', 
    'insurance', 'health', 'other'
]
```

### Logging Level

Set `LOG_LEVEL` in your `.env` file:
```env
LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR
```

### Rate Limiting

Adjust rate limiting in `config/settings.py`:
```python
RATE_LIMIT_DELAY = float(os.getenv('RATE_LIMIT_DELAY', '1.0'))
```

## 🔒 Security Considerations

- **Never commit your `.env` file** to version control
- **Keep your bot token private**
- **Use HTTPS for web app URLs**
- **AI analysis runs locally** for privacy

## 📱 Bot Features Overview

### Core Commands
- **Expense logging**: `6.60 coffee` or `25.50 lunch`
- **Statistics**: `/total`, `/stats`, `/recent`
- **Interactive reports**: `/monthly_report`, `/annual_report`
- **AI analysis**: `/analyze_monthly`, `/analyze_annual`

### AI Analysis Features
- **Flow-based processing** for accuracy
- **Pattern recognition** (e.g., "matcha 20 times")
- **Automatic categorization** of expenses
- **Insights and recommendations**
- **Local processing** for privacy

### Interactive Reports
- **Button-based interface** for easy navigation
- **Simple totals** for quick overview
- **AI analysis** for detailed insights
- **Automatic logging** of all analysis results

## 🎯 Next Steps

1. **Test all features** with the test scripts
2. **Customize categories** and settings
3. **Set up automated backups** of your Google Sheet
4. **Monitor bot usage** and logs
5. **Share with family/friends** for collaborative expense tracking

---

**Need help?** Check the troubleshooting section above or run the test scripts to identify any issues.

**Happy expense tracking! 💰📊**
