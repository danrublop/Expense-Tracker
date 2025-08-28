#!/usr/bin/env python3
"""
Test script for the Telegram Expense Logging Bot.
This script tests the core functionality without running the Telegram bot.
"""
import os
import sys
import logging
from bot.utils import parse_expense_message, validate_amount, validate_category
from sheets.operations import SheetOperations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_message_parsing():
    """Test the message parsing functionality."""
    print("🧪 Testing message parsing...")
    
    test_cases = [
        ("6.60 food", True, 6.60, "food"),
        ("9.70 coffee at starbucks", True, 9.70, "coffee at starbucks"),
        ("15.30 groceries", True, 15.30, "groceries"),
        ("125.00 gas", True, 125.00, "gas"),
        ("6,60 food", True, 6.60, "food"),  # Comma decimal
        ("6 food", True, 6.0, "food"),      # Integer amount
        ("0.50 snack", True, 0.50, "snack"), # Small amount
        ("1000000.00 rent", True, 1000000.00, "rent"), # Large amount
        
        # Invalid cases
        ("food", False, None, None),         # No amount
        ("6.60", False, None, None),        # No category
        ("abc food", False, None, None),    # Invalid amount
        ("-5.00 food", False, None, None),  # Negative amount
        ("", False, None, None),            # Empty message
        ("6.60", False, None, None),        # Missing category
    ]
    
    passed = 0
    total = len(test_cases)
    
    for message, should_succeed, expected_amount, expected_category in test_cases:
        amount, category, error_msg = parse_expense_message(message)
        
        if should_succeed:
            if amount == expected_amount and category == expected_category:
                print(f"✅ PASS: '{message}' → ${amount} for {category}")
                passed += 1
            else:
                print(f"❌ FAIL: '{message}' → Expected: ${expected_amount} for {expected_category}, Got: ${amount} for {category}")
        else:
            if error_msg:
                print(f"✅ PASS: '{message}' → Error: {error_msg}")
                passed += 1
            else:
                print(f"❌ FAIL: '{message}' → Expected error but got: ${amount} for {category}")
    
    print(f"\n📊 Message parsing: {passed}/{total} tests passed")
    return passed == total

def test_validation():
    """Test the validation functions."""
    print("\n🧪 Testing validation functions...")
    
    # Test amount validation
    amount_tests = [
        (6.60, True),
        (0.01, True),
        (1000000.00, True),
        (0, False),
        (-5.00, False),
        (1000001.00, False),
        ("abc", False),
    ]
    
    amount_passed = 0
    for amount, should_succeed in amount_tests:
        is_valid, error_msg = validate_amount(amount)
        if is_valid == should_succeed:
            print(f"✅ Amount validation: {amount} → {'Valid' if is_valid else 'Invalid'}")
            amount_passed += 1
        else:
            print(f"❌ Amount validation: {amount} → Expected: {should_succeed}, Got: {is_valid}")
    
    # Test category validation
    category_tests = [
        ("food", True),
        ("coffee at starbucks", True),
        ("", False),
        ("a" * 101, False),  # Too long
        ("<script>alert('xss')</script>", False),  # Harmful content
    ]
    
    category_passed = 0
    for category, should_succeed in category_tests:
        is_valid, error_msg = validate_category(category)
        if is_valid == should_succeed:
            print(f"✅ Category validation: '{category}' → {'Valid' if is_valid else 'Invalid'}")
            category_passed += 1
        else:
            print(f"❌ Category validation: '{category}' → Expected: {should_succeed}, Got: {is_valid}")
    
    total_validation_tests = len(amount_tests) + len(category_tests)
    total_passed = amount_passed + category_passed
    
    print(f"\n📊 Validation: {total_passed}/{total_validation_tests} tests passed")
    return total_passed == total_validation_tests

def test_sheets_connection():
    """Test the Google Sheets connection via Apps Script."""
    print("\n🧪 Testing Google Sheets connection...")
    
    try:
        sheet_ops = SheetOperations()
        
        if sheet_ops.is_connected():
            print("✅ Google Sheets connection successful")
            
            # Get connection info
            conn_info = sheet_ops.get_connection_info()
            print(f"📋 Spreadsheet ID: {conn_info['spreadsheet_id']}")
            print(f"🔗 Web App URL: {conn_info['webapp_url']}")
            
            return True
        else:
            print("❌ Google Sheets connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Google Sheets: {str(e)}")
        return False

def test_expense_logging():
    """Test logging an expense to Google Sheets via Apps Script."""
    print("\n🧪 Testing expense logging...")
    
    try:
        sheet_ops = SheetOperations()
        
        if not sheet_ops.is_connected():
            print("❌ Cannot test expense logging - sheets not connected")
            return False
        
        # Test logging a small expense
        test_amount = 0.01
        test_category = "test expense"
        
        success, message, running_total = sheet_ops.log_expense(test_amount, test_category)
        
        if success:
            print(f"✅ Test expense logged: {message}")
            print(f"💰 Running total: ${running_total}")
            return True
        else:
            print(f"❌ Failed to log test expense: {message}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing expense logging: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Telegram Expense Logging Bot - Test Suite")
    print("=" * 60)
    
    # Check if environment is configured
    if not os.path.exists('.env'):
        print("❌ .env file not found. Please run setup.py first.")
        return False
    
    # Check if required environment variables exist
    required_vars = ['TELEGRAM_BOT_TOKEN', 'SPREADSHEET_ID', 'WEBAPP_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and run setup.py if needed.")
        return False
    
    tests = [
        ("Message Parsing", test_message_parsing),
        ("Validation", test_validation),
        ("Google Sheets Connection", test_sheets_connection),
        ("Expense Logging", test_expense_logging),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the configuration and try again.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Testing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {str(e)}")
        sys.exit(1)
