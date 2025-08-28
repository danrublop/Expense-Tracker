# 🤖 Telegram Expense Tracker Bot

A **professional-grade Telegram bot** that automatically logs your expenses to Google Sheets with **AI-powered analysis**, **interactive reports**, and **smart categorization**. Features local Mistral LLM for privacy-focused financial insights.

## 🚀 Quick Start

1. **Clone and setup:**
   ```bash
   git clone https://github.com/danrublop/Expense-Tracker.git
   cd Expense-Tracker
   pip install -r requirements.txt
   ```

2. **Configure your bot:**
   ```bash
   cp env.example .env
   # Edit .env with your credentials (see SETUP_GUIDE.md)
   ```

3. **Set up Google Sheets:**
   ```bash
   python3 setup_google_sheets.py
   ```

4. **Test everything:**
   ```bash
   python3 test_bot.py
   python3 test_button_functionality.py
   ```

5. **Start your bot:**
   ```bash
   python3 main.py
   ```

📖 **Full setup guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)

## ✨ Features

### 💰 **Core Expense Tracking**
- **Natural language input**: Just send `6.60 food` or `9.70 coffee at starbucks`
- **Automatic Google Sheets integration**: Real-time expense logging
- **Running totals**: Each entry shows your cumulative spending
- **Smart parsing**: Handles amounts with dots or commas (6.60 or 6,60)
- **Category suggestions**: Get helpful category ideas
- **Professional formatting**: Currency formatting and clean layout

### 🤖 **AI-Powered Analysis**
- **Local Mistral LLM**: Privacy-focused AI processing via Ollama
- **Flow-based processing**: Multi-stage analysis for better accuracy
- **Smart categorization**: Automatically groups similar expenses
- **Pattern recognition**: Identifies recurring expenses (e.g., "matcha 20 times")
- **Financial insights**: AI-generated spending recommendations
- **Historical tracking**: All AI analysis results logged to sheets

### 📊 **Interactive Reports**
- **Button-based interface**: Easy navigation with inline keyboards
- **Monthly/Annual reports**: Choose between simple totals or AI analysis
- **Real-time statistics**: Live data from Google Sheets
- **Professional dashboards**: Clean, formatted reports

## 📋 Commands

- `/start` - Welcome message and instructions
- `/help` - Usage examples and tips
- `/total` - Show current total expenses
- `/stats` - Show spending statistics
- `/recent` - Show recent expenses
- `/monthly_report` - Interactive monthly report with button options
- `/annual_report` - Interactive annual report with button options
- `/analyze_monthly` - AI-powered monthly analysis
- `/analyze_annual` - AI-powered annual analysis

## 🔧 Setup Requirements

### Prerequisites
- Python 3.8+
- Telegram account
- Google account
- Google Sheets access
- **For AI Analysis**: Ollama installed and running locally

### Environment Variables
Create a `.env` file with:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
SPREADSHEET_ID=your_spreadsheet_id_here
WEBAPP_URL=your_webapp_url_here
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/danrublop/Expense-Tracker.git
   cd Expense-Tracker
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up Telegram bot:**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy the bot token to your `.env` file
   - **See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed BotFather setup**

4. **Set up Google Sheets:**
   - Run `python3 setup_google_sheets.py`
   - Follow the step-by-step instructions
   - This creates the Apps Script and deploys it

5. **Set up AI Analysis (optional):**
   ```bash
   # Install Ollama (see OLLAMA_SETUP.md for details)
   ollama serve
   ollama pull mistral
   
   # Test AI analysis
   python3 test_ai_analysis.py
   ```

6. **Test everything:**
   ```bash
   python3 test_bot.py
   ```

7. **Start the bot:**
   ```bash
   python3 main.py
   ```

## 📱 Usage Examples

### 💰 **Basic Expense Logging**
Send these messages to your bot:

```
6.60 food
9.70 coffee at starbucks
15.30 groceries
125.00 gas
```

The bot will:
- Parse the amount and description
- Log it to Google Sheets with timestamp
- Calculate running totals
- Format everything professionally
- Send confirmation messages

### 📊 **Interactive Reports**
Use these commands for detailed insights:

```
/monthly_report    # Shows button options for monthly analysis
/annual_report     # Shows button options for annual analysis
```

**Button Options:**
- **📊 Simple Total** - Quick expense summary
- **🤖 AI Analysis** - Full AI-powered insights

### 🤖 **AI Analysis Commands**
Direct AI analysis commands:

```
/analyze_monthly  # AI-powered monthly analysis
/analyze_annual   # AI-powered annual analysis
```

**AI Analysis Features:**
- **Flow 1**: Expense categorization
- **Flow 2**: Pattern recognition
- **Flow 3**: Insights & recommendations

## 🗂️ File Structure

```
finTELE/
├── bot/                    # Bot handlers and utilities
│   ├── handlers.py        # Message and command handlers
│   ├── utils.py           # Utility functions
│   └── ai_analysis.py     # AI analysis using Mistral LLM
├── config/                # Configuration files
│   ├── settings.py        # App settings and constants
│   └── credentials.example # Example credentials file
├── sheets/                # Google Sheets integration
│   ├── client.py          # HTTP client for Apps Script
│   └── operations.py      # Sheet operations logic
├── main.py                # Main bot entry point
├── test_bot.py            # Test suite
├── test_ai_analysis.py    # AI analysis test script
├── test_button_functionality.py # Button functionality test script
├── setup_google_sheets.py # Google Sheets setup script
├── ai_analysis_apps_script.js # Enhanced Apps Script for AI analysis
├── quick_start.py         # Quick start and status check
├── OLLAMA_SETUP.md        # Ollama setup guide
├── SETUP_GUIDE.md         # Complete setup guide
└── requirements.txt       # Python dependencies
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python3 test_bot.py
```

Tests cover:
- Message parsing
- Data validation
- Google Sheets connection
- Expense logging

### AI Analysis Testing

Test the AI analysis functionality:
```bash
python3 test_ai_analysis.py
```

This tests:
- Ollama connection
- Mistral model availability
- Monthly and annual analysis
- Report generation

### Interactive Report Testing

Test the new button-based report system:
```bash
python3 test_button_functionality.py
```

This tests:
- Report command registration
- Button handler setup
- Sheet operations integration
- AI analysis logging

## 🔍 Troubleshooting

### Common Issues

1. **"Bot not responding"**
   - Check your bot token in `.env`
   - Ensure bot is running (`python3 main.py`)
   - **See [SETUP_GUIDE.md](SETUP_GUIDE.md) for BotFather setup**

2. **"Google Sheets connection failed"**
   - Run `python3 setup_google_sheets.py`
   - Verify Apps Script deployment
   - Check Web App URL in `.env`

3. **"Apps Script error"**
   - Ensure spreadsheet has "Expenses" worksheet
   - Check Apps Script code is correct
   - Verify deployment settings

4. **"AI Analysis not working"**
   - Ensure Ollama is running: `ollama serve`
   - Check Mistral model: `ollama list`
   - Pull model if missing: `ollama pull mistral`
   - See `OLLAMA_SETUP.md` for detailed setup

### Getting Help

1. **Check logs**: Look at `bot.log` for detailed error messages
2. **Run tests**: `python3 test_bot.py` to identify issues
3. **Verify setup**: `python3 quick_start.py` to check configuration
4. **Check Google Apps Script**: Look for errors in the Apps Script console
5. **Follow setup guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Follow the [SETUP_GUIDE.md](SETUP_GUIDE.md) step by step
3. Run the test suite to identify problems
4. Check the logs for detailed error messages
5. Verify your Google Sheets and Apps Script setup

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
- **[OLLAMA_SETUP.md](OLLAMA_SETUP.md)** - AI analysis setup guide
- **This README** - Feature overview and quick start

---

**Happy expense tracking! 💰📊**

**Need help?** Start with [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed step-by-step instructions.
