/**
 * Google Apps Script for AI Analysis Integration
 * This script handles AI analysis logging and data extraction
 */

// Global variables
const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
const EXPENSES_SHEET_NAME = 'Expenses';
const AI_ANALYSIS_SHEET_NAME = 'AI Analysis';

/**
 * Log AI analysis results to the AI Analysis worksheet
 * @param {Object} analysisData - The analysis data to log
 * @return {Object} Success status and message
 */
function logAIAnalysis(analysisData) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    let aiSheet = spreadsheet.getSheetByName(AI_ANALYSIS_SHEET_NAME);
    
    // Create AI Analysis sheet if it doesn't exist
    if (!aiSheet) {
      aiSheet = createAIAnalysisSheet(spreadsheet);
    }
    
    // Prepare data for logging
    const rowData = [
      analysisData.date,
      analysisData.time,
      analysisData.period,
      analysisData.total_expenses,
      analysisData.total_transactions,
      analysisData.categories_count,
      analysisData.insights_count,
      analysisData.recommendations_count,
      analysisData.analysis_date,
      new Date() // Timestamp when logged
    ];
    
    // Append the data
    aiSheet.appendRow(rowData);
    
    // Auto-resize columns
    aiSheet.autoResizeColumns(1, rowData.length);
    
    return {
      success: true,
      message: 'AI analysis logged successfully'
    };
    
  } catch (error) {
    console.error('Error logging AI analysis:', error);
    return {
      success: false,
      message: 'Failed to log AI analysis: ' + error.toString()
    };
  }
}

/**
 * Create the AI Analysis worksheet with proper headers
 * @param {Spreadsheet} spreadsheet - The spreadsheet object
 * @return {Sheet} The created sheet
 */
function createAIAnalysisSheet(spreadsheet) {
  const sheet = spreadsheet.insertSheet(AI_ANALYSIS_SHEET_NAME);
  
  // Set headers
  const headers = [
    'Date',
    'Time', 
    'Period',
    'Total Expenses',
    'Total Transactions',
    'Categories Count',
    'Insights Count',
    'Recommendations Count',
    'Analysis Date',
    'Logged At'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  
  // Style the header row
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight('bold');
  headerRange.setBackground('#f0f0f0');
  headerRange.setHorizontalAlignment('center');
  
  // Freeze the header row
  sheet.setFrozenRows(1);
  
  // Set number formats
  sheet.getRange(2, 4, 1000, 1).setNumberFormat('$#,##0.00'); // Total Expenses
  sheet.getRange(2, 5, 1000, 1).setNumberFormat('#,##0'); // Total Transactions
  sheet.getRange(2, 6, 1000, 1).setNumberFormat('#,##0'); // Categories Count
  sheet.getRange(2, 7, 1000, 1).setNumberFormat('#,##0'); // Insights Count
  sheet.getRange(2, 8, 1000, 1).setNumberFormat('#,##0'); // Recommendations Count
  
  // Set date formats
  sheet.getRange(2, 1, 1000, 1).setNumberFormat('yyyy-mm-dd'); // Date
  sheet.getRange(2, 2, 1000, 1).setNumberFormat('hh:mm:ss'); // Time
  sheet.getRange(2, 9, 1000, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss'); // Analysis Date
  sheet.getRange(2, 10, 1000, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss'); // Logged At
  
  return sheet;
}

/**
 * Extract expense data for AI analysis
 * @param {string} period - 'monthly' or 'annual'
 * @return {Object} Success status, message, and expense data
 */
function getExpenseDataForAnalysis(period) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const expensesSheet = spreadsheet.getSheetByName(EXPENSES_SHEET_NAME);
    
    if (!expensesSheet) {
      return {
        success: false,
        message: 'Expenses sheet not found',
        data: []
      };
    }
    
    // Get all data from expenses sheet
    const data = expensesSheet.getDataRange().getValues();
    
    if (data.length <= 1) { // Only header row
      return {
        success: false,
        message: 'No expense data found',
        data: []
      };
    }
    
    // Skip header row and process data
    const expenses = [];
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      const date = row[0]; // Date column
      const amount = row[2]; // Amount column
      const description = row[3]; // Category/Description column
      
      // Filter by period
      if (period === 'monthly') {
        const currentDate = new Date();
        const expenseDate = new Date(date);
        if (expenseDate.getMonth() === currentDate.getMonth() && 
            expenseDate.getFullYear() === currentDate.getFullYear()) {
          expenses.push({
            date: date,
            amount: amount,
            description: description
          });
        }
      } else if (period === 'annual') {
        const currentDate = new Date();
        const expenseDate = new Date(date);
        if (expenseDate.getFullYear() === currentDate.getFullYear()) {
          expenses.push({
            date: date,
            amount: amount,
            description: description
          });
        }
      }
    }
    
    return {
      success: true,
      message: `Found ${expenses.length} expenses for ${period} period`,
      data: expenses
    };
    
  } catch (error) {
    console.error('Error getting expense data for analysis:', error);
    return {
      success: false,
      message: 'Failed to get expense data: ' + error.toString(),
      data: []
    };
  }
}

/**
 * Get monthly statistics for simple reports
 * @param {string} month - Month identifier ('current' or 'annual')
 * @return {Object} Success status, message, and statistics
 */
function getMonthlyStats(month) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const expensesSheet = spreadsheet.getSheetByName(EXPENSES_SHEET_NAME);
    
    if (!expensesSheet) {
      return {
        success: false,
        message: 'Expenses sheet not found',
        stats: {}
      };
    }
    
    // Get all data from expenses sheet
    const data = expensesSheet.getDataRange().getValues();
    
    if (data.length <= 1) { // Only header row
      return {
        success: false,
        message: 'No expense data found',
        stats: {}
      };
    }
    
    let totalAmount = 0;
    let transactionCount = 0;
    const currentDate = new Date();
    
    // Process data based on month parameter
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      const date = new Date(row[0]);
      const amount = parseFloat(row[2]) || 0;
      
      let includeExpense = false;
      
      if (month === 'current') {
        // Current month
        includeExpense = (date.getMonth() === currentDate.getMonth() && 
                         date.getFullYear() === currentDate.getFullYear());
      } else if (month === 'annual') {
        // Current year
        includeExpense = (date.getFullYear() === currentDate.getFullYear());
      }
      
      if (includeExpense) {
        totalAmount += amount;
        transactionCount++;
      }
    }
    
    const stats = {
      totalAmount: totalAmount,
      transactionCount: transactionCount,
      period: month === 'current' ? 'Current Month' : 'Current Year'
    };
    
    return {
      success: true,
      message: `📊 **${stats.period} Statistics**\n\n` +
               `💰 **Total Expenses**: $${totalAmount.toFixed(2)}\n` +
               `🔢 **Total Transactions**: ${transactionCount}\n` +
               `📅 **Period**: ${month === 'current' ? 'This Month' : 'This Year'}`,
      stats: stats
    };
    
  } catch (error) {
    console.error('Error getting monthly stats:', error);
    return {
      success: false,
      message: 'Failed to get statistics: ' + error.toString(),
      stats: {}
    };
  }
}

/**
 * Main function to handle web app requests
 * @param {Object} e - The event object from the web app
 * @return {Object} Response object
 */
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const action = data.action;
    
    switch (action) {
      case 'logAIAnalysis':
        return logAIAnalysis(data.analysisData);
        
      case 'getExpenseDataForAnalysis':
        return getExpenseDataForAnalysis(data.period);
        
      case 'getMonthlyStats':
        return getMonthlyStats(data.month);
        
      default:
        return {
          success: false,
          message: 'Unknown action: ' + action
        };
    }
    
  } catch (error) {
    console.error('Error in doPost:', error);
    return {
      success: false,
      message: 'Error processing request: ' + error.toString()
    };
  }
}

/**
 * Test function to verify the script is working
 * @return {string} Test result message
 */
function testAIAnalysisScript() {
  try {
    // Test creating AI Analysis sheet
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    let aiSheet = spreadsheet.getSheetByName(AI_ANALYSIS_SHEET_NAME);
    
    if (!aiSheet) {
      aiSheet = createAIAnalysisSheet(spreadsheet);
      console.log('AI Analysis sheet created successfully');
    } else {
      console.log('AI Analysis sheet already exists');
    }
    
    // Test getting expense data
    const monthlyData = getExpenseDataForAnalysis('monthly');
    console.log('Monthly data test:', monthlyData);
    
    const annualData = getExpenseDataForAnalysis('annual');
    console.log('Annual data test:', annualData);
    
    // Test getting stats
    const currentStats = getMonthlyStats('current');
    console.log('Current month stats test:', currentStats);
    
    return 'AI Analysis script test completed successfully!';
    
  } catch (error) {
    console.error('Test failed:', error);
    return 'Test failed: ' + error.toString();
  }
}
