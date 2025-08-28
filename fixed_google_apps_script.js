function doPost(e) {
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
}