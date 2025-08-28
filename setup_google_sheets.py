#!/usr/bin/env python3
"""
Google Sheets and Apps Script Setup Script for Telegram Expense Logging Bot
"""
import os
import sys
import webbrowser
from pathlib import Path

def print_header():
    """Print the setup header."""
    print("=" * 60)
    print("🔧 Google Sheets & Apps Script Setup")
    print("=" * 60)
    print()

def print_step(step_num, title):
    """Print a step header."""
    print(f"📋 Step {step_num}: {title}")
    print("-" * 40)

def print_instructions(instructions):
    """Print formatted instructions."""
    for line in instructions:
        print(f"  {line}")
    print()

def create_apps_script_code():
    """Create the Apps Script code file."""
    script_code = '''function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Expenses");
    const data = JSON.parse(e.postData.contents);
    
    // Add headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["Date", "Time", "Amount", "Category", "Running Total"]);
      sheet.getRange(1, 1, 1, 5).setFontWeight("bold");
      sheet.getRange(1, 1, 1, 5).setHorizontalAlignment("center");
      sheet.getRange(1, 1, 1, 5).setBackground("#e6e6e6");
    }
    
    const { amount, category } = data;
    const now = new Date();
    const date = Utilities.formatDate(now, "GMT", "yyyy-MM-dd");
    const time = Utilities.formatDate(now, "GMT", "HH:mm");
    
    // Calculate running total
    let runningTotal = 0;
    if (sheet.getLastRow() > 1) {
      const lastTotal = sheet.getRange(sheet.getLastRow(), 5).getValue();
      runningTotal = lastTotal + parseFloat(amount);
    } else {
      runningTotal = parseFloat(amount);
    }
    
    // Add the expense row
    sheet.appendRow([date, time, parseFloat(amount), category, runningTotal]);
    
    // Format the amount and total columns as currency
    const rowNum = sheet.getLastRow();
    sheet.getRange(rowNum, 3).setNumberFormat("$#,##0.00");
    sheet.getRange(rowNum, 5).setNumberFormat("$#,##0.00");
    
    // Set column widths
    sheet.setColumnWidth(1, 100); // Date
    sheet.setColumnWidth(2, 80);  // Time
    sheet.setColumnWidth(3, 100); // Amount
    sheet.setColumnWidth(4, 200); // Category
    sheet.setColumnWidth(5, 120); // Running Total
    
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: `Logged $${amount} for ${category}`,
      runningTotal: runningTotal
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput("Expense Logger Bot is running!");
}'''
    
    # Create the file
    script_file = Path("google_apps_script.js")
    with open(script_file, "w") as f:
        f.write(script_code)
    
    print(f"✅ Created Apps Script file: {script_file}")
    return script_file

def main():
    """Main setup function."""
    print_header()
    
    print("This script will help you set up Google Sheets and Apps Script for your bot.")
    print("You'll need to manually complete some steps in Google's web interface.")
    print()
    
    # Step 1: Create Google Sheet
    print_step(1, "Create Google Sheet")
    instructions = [
        "1. Go to https://sheets.google.com/",
        "2. Create a NEW spreadsheet",
        "3. Rename the first worksheet to 'Expenses'",
        "4. Save the spreadsheet with a descriptive name"
    ]
    print_instructions(instructions)
    
    input("Press Enter when you've created the Google Sheet...")
    
    # Step 2: Get Spreadsheet ID
    print_step(2, "Get Spreadsheet ID")
    instructions = [
        "1. In your Google Sheet, look at the URL:",
        "   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit",
        "2. Copy the SPREADSHEET_ID (the long string between /d/ and /edit)",
        "3. Save this ID - you'll need it for your .env file"
    ]
    print_instructions(instructions)
    
    spreadsheet_id = input("Enter your Spreadsheet ID: ").strip()
    if not spreadsheet_id:
        print("❌ Spreadsheet ID is required!")
        return
    
    # Step 3: Create Apps Script
    print_step(3, "Create Apps Script")
    instructions = [
        "1. In your Google Sheet, go to Extensions → Apps Script",
        "2. Delete any existing code in the editor",
        "3. Copy the code from the file I'll create for you",
        "4. Save the script (Ctrl+S or Cmd+S)"
    ]
    print_instructions(instructions)
    
    script_file = create_apps_script_code()
    print(f"📄 Open this file and copy the code: {script_file.absolute()}")
    
    input("Press Enter when you've copied the code to Apps Script...")
    
    # Step 4: Deploy Apps Script
    print_step(4, "Deploy Apps Script")
    instructions = [
        "1. In Apps Script, click 'Deploy' → 'New deployment'",
        "2. Choose 'Web app' as type",
        "3. Set 'Execute as' to 'Me'",
        "4. Set 'Who has access' to 'Anyone'",
        "5. Click 'Deploy'",
        "6. Authorize the app when prompted",
        "7. Copy the Web App URL that appears"
    ]
    print_instructions(instructions)
    
    webapp_url = input("Enter your Web App URL: ").strip()
    if not webapp_url:
        print("❌ Web App URL is required!")
        return
    
    # Step 5: Update .env file
    print_step(5, "Update Environment Variables")
    
    # Check if .env exists
    env_file = Path(".env")
    if env_file.exists():
        print("📝 Updating existing .env file...")
        # Read current .env content
        with open(env_file, "r") as f:
            content = f.read()
        
        # Update the values
        lines = content.split('\n')
        updated_lines = []
        for line in lines:
            if line.startswith('SPREADSHEET_ID='):
                updated_lines.append(f'SPREADSHEET_ID={spreadsheet_id}')
            elif line.startswith('WEBAPP_URL='):
                updated_lines.append(f'WEBAPP_URL={webapp_url}')
            else:
                updated_lines.append(line)
        
        # Write back
        with open(env_file, "w") as f:
            f.write('\n'.join(updated_lines))
    else:
        print("❌ .env file not found! Please run the main setup.py first.")
        return
    
    print("✅ Updated .env file with your Google Sheets configuration!")
    
    # Step 6: Test the setup
    print_step(6, "Test Your Setup")
    instructions = [
        "1. Run: python3 test_bot.py",
        "2. Check that all tests pass",
        "3. If tests pass, run: python3 main.py",
        "4. Test your bot on Telegram!"
    ]
    print_instructions(instructions)
    
    print("🎉 Setup complete! Your Google Sheets integration should now work.")
    print()
    print("📚 Next steps:")
    print("  • Test with: python3 test_bot.py")
    print("  • Run bot with: python3 main.py")
    print("  • Send '/start' to your bot on Telegram")
    print("  • Try logging an expense: '6.60 food'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Setup failed: {str(e)}")
        sys.exit(1)
