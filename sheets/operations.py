"""
Sheet operations for the Telegram Expense Logging Bot.
"""
from datetime import datetime
from typing import Tuple, Optional, Dict, List, Any
import logging
from sheets.client import SimpleSheetsClient
from config.settings import DATE_FORMAT, TIME_FORMAT

logger = logging.getLogger(__name__)

class SheetOperations:
    """Handles all sheet operations for expense logging."""
    
    def __init__(self):
        """Initialize the sheet operations."""
        self.client = SimpleSheetsClient()
    
    def log_expense(self, amount: float, category: str) -> Tuple[bool, str, float]:
        """
        Log an expense to the main expenses worksheet.
        
        Args:
            amount: The expense amount
            category: The expense category/description
            
        Returns:
            Tuple of (success, message, running_total)
        """
        try:
            # Log the expense via Apps Script
            result = self.client.log_expense(amount, category)
            
            if result['success']:
                message = f"✅ Logged ${amount:.2f} for {category}. Running total: ${result['running_total']:.2f}"
                logger.info(f"Successfully logged expense: ${amount} for {category}")
                return True, message, result['running_total']
            else:
                error_msg = f"❌ Failed to log expense: {result['message']}"
                logger.error(f"Failed to log expense: ${amount} for {category}")
                return False, error_msg, 0.0
                
        except Exception as e:
            error_msg = f"❌ Error logging expense: {str(e)}"
            logger.error(f"Exception while logging expense: {str(e)}")
            return False, error_msg, 0.0
    
    def get_current_total(self) -> Tuple[bool, str, float]:
        """
        Get the current total amount of all expenses.
        Note: This requires the Apps Script to support GET requests for totals.
        
        Returns:
            Tuple of (success, message, total)
        """
        try:
            # For now, we'll return a message that the total is shown in the sheet
            # The Apps Script calculates and displays the running total automatically
            message = "💰 Check your Google Sheet for the current running total. Each expense row shows the cumulative total."
            
            return True, message, 0.0
            
        except Exception as e:
            error_msg = f"❌ Error getting total: {str(e)}"
            logger.error(f"Exception while getting total: {str(e)}")
            return False, error_msg, 0.0
    
    def get_monthly_stats(self, month: Optional[str] = None) -> Tuple[bool, str, Dict]:
        """
        Get basic statistics information.
        
        Args:
            month: Month identifier ('current', 'annual', or specific month)
            
        Returns:
            Tuple of (success, message, stats_dict)
        """
        try:
            # Determine which period to get stats for
            if month == "current":
                period = "current"
            elif month == "annual":
                period = "annual"
            else:
                # For specific months, use the existing logic
                if month:
                    message = f"📊 **{month} Statistics**\n\n"
                    message += "📋 **View your Google Sheet** for detailed statistics:\n"
                    message += "• Total expenses and amounts\n"
                    message += "• Category breakdowns\n"
                    message += "• Monthly trends\n"
                    message += "• Running totals\n\n"
                    message += "💡 **Tip**: Use Google Sheets' built-in features like:\n"
                    message += "• SUM() functions for totals\n"
                    message += "• Pivot tables for analysis\n"
                    message += "• Charts for visualization"
                else:
                    message = "📊 **All Time Statistics**\n\n"
                    message += "📋 **View your Google Sheet** for complete statistics:\n"
                    message += "• All expenses with dates and times\n"
                    message += "• Running totals for each entry\n"
                    message += "• Category breakdowns\n"
                    message += "• Spending patterns over time\n\n"
                    message += "💡 **Tip**: The Apps Script automatically:\n"
                    message += "• Calculates running totals\n"
                    message += "• Formats amounts as currency\n"
                    message += "• Organizes data chronologically"
                
                stats = {
                    'month': month,
                    'message': message,
                    'note': 'Statistics are available in the Google Sheet'
                }
                return True, message, stats
            
            # Call the Apps Script for current/annual stats
            result = self.client.call_apps_script_function(
                'getMonthlyStats',
                {'month': period}
            )
            
            if result.get('success'):
                message = result.get('message', 'Statistics retrieved successfully')
                stats = result.get('stats', {})
                return True, message, stats
            else:
                return False, result.get('message', 'Failed to get statistics'), {}
                
        except Exception as e:
            error_msg = f"❌ Error getting statistics: {str(e)}"
            logger.error(f"Exception while getting statistics: {str(e)}")
            return False, error_msg, {}
    
    def get_recent_expenses(self, limit: int = 5) -> Tuple[bool, str, List]:
        """
        Get information about recent expenses.
        Note: Recent expenses are visible in the Google Sheet.
        
        Args:
            limit: Maximum number of recent expenses to return
            
        Returns:
            Tuple of (success, message, expenses_list)
        """
        try:
            message = "📝 **Recent Expenses**\n\n"
            message += f"📋 **Check your Google Sheet** for the last {limit} expenses.\n"
            message += "The most recent expenses appear at the bottom of the sheet.\n\n"
            message += "💡 **Features in your sheet**:\n"
            message += "• Automatic date and time stamps\n"
            message += "• Running totals for each entry\n"
            message += "• Currency formatting\n"
            message += "• Professional header styling\n\n"
            message += "🔗 **Access your sheet**:\n"
            message += f"https://docs.google.com/spreadsheets/d/{self.client.spreadsheet_id}/edit"
            
            return True, message, []
            
        except Exception as e:
            error_msg = f"❌ Error getting recent expenses: {str(e)}"
            logger.error(f"Exception while getting recent expenses: {str(e)}")
            return False, error_msg, []
    
    def get_expense_data_for_analysis(self, period: str = 'monthly') -> Tuple[bool, str, List[Dict]]:
        """
        Get expense data for AI analysis.
        
        Args:
            period: 'monthly' or 'annual'
            
        Returns:
            Tuple of (success, message, expense_data)
        """
        try:
            # Call the Apps Script to get expense data
            result = self.client.call_apps_script_function(
                'getExpenseDataForAnalysis',
                {'period': period}
            )
            
            if result.get('success'):
                expense_data = result.get('data', [])
                message = result.get('message', f'Retrieved {len(expense_data)} expenses for {period} period')
                return True, message, expense_data
            else:
                return False, result.get('message', 'Failed to get expense data'), []
                
        except Exception as e:
            error_msg = f"❌ Error getting expense data for analysis: {str(e)}"
            logger.error(f"Exception while getting expense data for analysis: {str(e)}")
            return False, error_msg, []
    
    def log_ai_analysis(self, analysis_data: Dict[str, Any]) -> bool:
        """
        Log AI analysis results to the AI Analysis worksheet.
        
        Args:
            analysis_data: Dictionary containing analysis results
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Call the Apps Script to log AI analysis
            result = self.client.call_apps_script_function(
                'logAIAnalysis',
                {'analysisData': analysis_data}
            )
            
            if result.get('success'):
                logger.info(f"AI analysis logged to sheets: {result.get('message')}")
                return True
            else:
                logger.warning(f"Failed to log AI analysis: {result.get('message')}")
                return False
                
        except Exception as e:
            logger.error(f"Error logging AI analysis: {str(e)}")
            return False
    
    def validate_expense_data(self, amount: float, category: str) -> Tuple[bool, str]:
        """
        Validate expense data before logging.
        
        Args:
            amount: The expense amount
            category: The expense category/description
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if amount <= 0:
            return False, "❌ Amount must be greater than 0."
        
        if amount > 1000000:  # $1M limit
            return False, "❌ Amount seems too high. Please check and try again."
        
        if not category or not category.strip():
            return False, "❌ Please provide a description for your expense."
        
        if len(category.strip()) > 100:
            return False, "❌ Description is too long. Please keep it under 100 characters."
        
        return True, ""
    
    def is_connected(self) -> bool:
        """
        Check if the sheet operations are connected to the Apps Script web app.
        
        Returns:
            True if connected, False otherwise
        """
        return self.client.is_connected()
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get connection information for debugging.
        
        Returns:
            Dictionary with connection details
        """
        return self.client.get_spreadsheet_info()
