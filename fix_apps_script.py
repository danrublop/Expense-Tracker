#!/usr/bin/env python3
"""
Fix Google Apps Script Issues
"""
import os
import sys
from pathlib import Path

def print_header():
    """Print the fix header."""
    print("=" * 60)
    print("🔧 Fix Google Apps Script Issues")
    print("=" * 60)
    print()

def create_fixed_apps_script():
    """Create a fixed version of the Apps Script code."""
    fixed_script = '''function doPost(e) {
  try {
    // Get the active spreadsheet
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    if (!spreadsheet) {
      throw new Error("No active spreadsheet found");
    }
    
    // Get or create the Expenses worksheet
    let sheet = spreadsheet.getSheetByName("Expenses");
    if (!sheet) {
      // Create the Expenses worksheet if it doesn't exist
      sheet = spreadsheet.insertSheet("Expenses");
      console.log("Created new Expenses worksheet");
    }
    
    // Ensure the sheet exists and is accessible
    if (!sheet) {
      throw new Error("Failed to create or access Expenses worksheet");
    }
    
    const data = JSON.parse(e.postData.contents);
    const { amount, category } = data;
    
    // Validate input data
    if (!amount || !category) {
      throw new Error("Missing amount or category");
    }
    
    // Add headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["Date", "Time", "Amount", "Category", "Running Total"]);
      sheet.getRange(1, 1, 1, 5).setFontWeight("bold");
      sheet.getRange(1, 1, 1, 5).setHorizontalAlignment("center");
      sheet.getRange(1, 1, 1, 5).setBackground("#e6e6e6");
      console.log("Added headers to worksheet");
    }
    
    const now = new Date();
    const date = Utilities.formatDate(now, "GMT", "yyyy-MM-dd");
    const time = Utilities.formatDate(now, "GMT", "HH:mm");
    
    // Calculate running total
    let runningTotal = 0;
    if (sheet.getLastRow() > 1) {
      try {
        const lastTotal = sheet.getRange(sheet.getLastRow(), 5).getValue();
        runningTotal = (lastTotal || 0) + parseFloat(amount);
      } catch (error) {
        console.log("Error getting last total, starting from 0: " + error);
        runningTotal = parseFloat(amount);
      }
    } else {
      runningTotal = parseFloat(amount);
    }
    
    // Add the expense row
    sheet.appendRow([date, time, parseFloat(amount), category, runningTotal]);
    console.log("Added expense row: " + amount + " for " + category);
    
    // Format the amount and total columns as currency
    const rowNum = sheet.getLastRow();
    try {
      sheet.getRange(rowNum, 3).setNumberFormat("$#,##0.00");
      sheet.getRange(rowNum, 5).setNumberFormat("$#,##0.00");
    } catch (error) {
      console.log("Error formatting currency: " + error);
    }
    
    // Set column widths
    try {
      sheet.setColumnWidth(1, 100); // Date
      sheet.setColumnWidth(2, 80);  // Time
      sheet.setColumnWidth(3, 100); // Amount
      sheet.setColumnWidth(4, 200); // Category
      sheet.setColumnWidth(5, 120); // Running Total
    } catch (error) {
      console.log("Error setting column widths: " + error);
    }
    
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: `Logged $${amount} for ${category}`,
      runningTotal: runningTotal
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    console.error("Error in doPost: " + error.toString());
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    if (!spreadsheet) {
      return ContentService.createTextOutput("No active spreadsheet found");
    }
    
    const sheet = spreadsheet.getSheetByName("Expenses");
    if (!sheet) {
      return ContentService.createTextOutput("Expenses worksheet not found");
    }
    
    return ContentService.createTextOutput("Expense Logger Bot is running! Sheet: " + sheet.getName());
  } catch (error) {
    return ContentService.createTextOutput("Error: " + error.toString());
  }
}

function setupSheet() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    if (!spreadsheet) {
      throw new Error("No active spreadsheet found");
    }
    
    // Get or create the Expenses worksheet
    let sheet = spreadsheet.getSheetByName("Expenses");
    if (!sheet) {
      sheet = spreadsheet.insertSheet("Expenses");
    }
    
    // Clear existing content
    sheet.clear();
    
    // Add headers
    sheet.appendRow(["Date", "Time", "Amount", "Category", "Running Total"]);
    sheet.getRange(1, 1, 1, 5).setFontWeight("bold");
    sheet.getRange(1, 1, 1, 5).setHorizontalAlignment("center");
    sheet.getRange(1, 1, 1, 5).setBackground("#e6e6e6");
    
    // Set column widths
    sheet.setColumnWidth(1, 100); // Date
    sheet.setColumnWidth(2, 80);  // Time
    sheet.setColumnWidth(3, 100); // Amount
    sheet.setColumnWidth(4, 200); // Category
    sheet.setColumnWidth(5, 120); // Running Total
    
    console.log("Sheet setup completed successfully");
    return "Sheet setup completed successfully";
    
  } catch (error) {
    console.error("Error in setupSheet: " + error.toString());
    throw error;
  }
}'''
    
    # Create the file
    script_file = Path("fixed_google_apps_script.js")
    with open(script_file, "w") as f:
        f.write(fixed_script)
    
    print(f"✅ Created fixed Apps Script file: {script_file}")
    return script_file

def main():
    """Main fix function."""
    print_header()
    
    print("The issue is likely that your Google Apps Script needs to be updated.")
    print("The current script has some error handling issues.")
    print()
    
    # Create the fixed script
    script_file = create_fixed_apps_script()
    
    print("\n📋 To fix this issue:")
    print("1. Open your Google Sheet")
    print("2. Go to Extensions → Apps Script")
    print("3. Replace ALL the code with the contents of:")
    print(f"   {script_file.absolute()}")
    print("4. Save the script (Ctrl+S or Cmd+S)")
    print("5. Deploy again:")
    print("   - Click 'Deploy' → 'New deployment'")
    print("   - Choose 'Web app' as type")
    print("   - Set 'Execute as' to 'Me'")
    print("   - Set 'Who has access' to 'Anyone'")
    print("   - Click 'Deploy'")
    print("6. Copy the new Web App URL")
    print("7. Update your .env file with the new URL")
    print()
    
    print("💡 Alternative: You can also run the setup script again:")
    print("   python3 setup_google_sheets.py")
    print()
    
    print("🔍 The main fixes in this version:")
    print("  • Better error handling for missing worksheets")
    print("  • Automatic worksheet creation if it doesn't exist")
    print("  • More robust running total calculation")
    print("  • Better logging and debugging")
    print("  • Added setupSheet() function for manual setup")
    
    print("\n📄 The fixed script file is ready at:")
    print(f"   {script_file.absolute()}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Fix cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Fix failed: {str(e)}")
        sys.exit(1)
