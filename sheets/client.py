"""
Simple HTTP client for the Telegram Expense Logging Bot using Google Apps Script.
"""
import requests
import logging
from typing import Optional, Dict, Any
from config.settings import SPREADSHEET_ID, WEBAPP_URL

logger = logging.getLogger(__name__)

class SimpleSheetsClient:
    """Simple client for interacting with Google Sheets via Apps Script."""
    
    def __init__(self):
        """Initialize the simple sheets client."""
        self.webapp_url = WEBAPP_URL
        self.spreadsheet_id = SPREADSHEET_ID
        
        if not self.webapp_url:
            raise ValueError("WEBAPP_URL environment variable is required")
        
        if not self.spreadsheet_id:
            raise ValueError("SPREADSHEET_ID environment variable is required")
    
    def log_expense(self, amount: float, category: str) -> Dict[str, Any]:
        """
        Log an expense via the Apps Script web app.
        
        Args:
            amount: The expense amount
            category: The expense category/description
            
        Returns:
            Response dictionary with success status and data
        """
        try:
            payload = {
                'amount': amount,
                'category': category
            }
            
            response = requests.post(self.webapp_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    logger.info(f"Successfully logged expense: ${amount} for {category}")
                    return {
                        'success': True,
                        'message': result.get('message', 'Expense logged successfully'),
                        'running_total': result.get('runningTotal', 0)
                    }
                else:
                    logger.error(f"Apps Script error: {result.get('error', 'Unknown error')}")
                    return {
                        'success': False,
                        'message': f"Apps Script error: {result.get('error', 'Unknown error')}",
                        'running_total': 0
                    }
            else:
                logger.error(f"HTTP error {response.status_code}: {response.text}")
                return {
                    'success': False,
                    'message': f"HTTP error {response.status_code}",
                    'running_total': 0
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return {
                'success': False,
                'message': f"Request failed: {str(e)}",
                'running_total': 0
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'success': False,
                'message': f"Unexpected error: {str(e)}",
                'running_total': 0
            }
    
    def test_connection(self) -> bool:
        """
        Test the connection to the Apps Script web app.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = requests.get(self.webapp_url, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Apps Script web app connection successful")
                return True
            else:
                logger.error(f"❌ Apps Script web app connection failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Apps Script web app connection failed: {str(e)}")
            return False
    
    def is_connected(self) -> bool:
        """
        Check if the client is connected to the Apps Script web app.
        
        Returns:
            True if connected, False otherwise
        """
        return self.test_connection()
    
    def get_spreadsheet_info(self) -> Dict[str, Any]:
        """
        Get basic information about the spreadsheet.
        
        Returns:
            Dictionary with spreadsheet information
        """
        return {
            'spreadsheet_id': self.spreadsheet_id,
            'webapp_url': self.webapp_url,
            'connection_status': 'connected' if self.is_connected() else 'disconnected'
        }
    
    def call_apps_script_function(self, function_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a specific Apps Script function with parameters.
        
        Args:
            function_name: Name of the function to call
            params: Parameters to pass to the function
            
        Returns:
            Response dictionary with success status and data
        """
        try:
            payload = {
                'action': function_name,
                **params
            }
            
            response = requests.post(self.webapp_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    logger.info(f"Successfully called {function_name}")
                    return result
                else:
                    logger.error(f"Apps Script error in {function_name}: {result.get('message', 'Unknown error')}")
                    return result
            else:
                logger.error(f"HTTP error {response.status_code}: {response.text}")
                return {
                    'success': False,
                    'message': f"HTTP error {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {function_name}: {str(e)}")
            return {
                'success': False,
                'message': f"Request failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error in {function_name}: {str(e)}")
            return {
                'success': False,
                'message': f"Unexpected error: {str(e)}"
            }