"""
Message and command handlers for the Telegram Expense Logging Bot.
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
import logging
from typing import Union
from datetime import datetime
from bot.utils import (
    parse_expense_message, is_command, extract_command_args,
    format_category_suggestions
)
from sheets.operations import SheetOperations
from bot.ai_analysis import MistralAnalyzer
from config.settings import (
    WELCOME_MESSAGE, HELP_MESSAGE, ERROR_INVALID_FORMAT,
    ERROR_SHEETS_API
)

logger = logging.getLogger(__name__)

class BotHandlers:
    """Handles all bot interactions and commands."""
    
    def __init__(self):
        """Initialize the bot handlers."""
        self.sheet_ops = SheetOperations()
        self.ai_analyzer = None  # Initialize lazily when needed
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        try:
            await update.message.reply_text(
                WELCOME_MESSAGE,
                parse_mode='Markdown'
            )
            logger.info(f"User {update.effective_user.id} started the bot")
        except Exception as e:
            logger.error(f"Error in start command: {str(e)}")
            await update.message.reply_text("❌ Error starting bot. Please try again.")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command."""
        try:
            await update.message.reply_text(
                HELP_MESSAGE,
                parse_mode='Markdown'
            )
            logger.info(f"User {update.effective_user.id} requested help")
        except Exception as e:
            logger.error(f"Error in help command: {str(e)}")
            await update.message.reply_text("❌ Error showing help. Please try again.")
    
    async def total_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /total command to show total expenses."""
        try:
            if not self.sheet_ops.is_connected():
                await update.message.reply_text(ERROR_SHEETS_API)
                return
            
            success, message, total = self.sheet_ops.get_current_total()
            
            if success:
                await update.message.reply_text(message)
                logger.info(f"User {update.effective_user.id} requested total: ${total}")
            else:
                await update.message.reply_text(message)
                logger.warning(f"Failed to get total for user {update.effective_user.id}")
                
        except Exception as e:
            logger.error(f"Error in total command: {str(e)}")
            await update.message.reply_text("❌ Error getting total. Please try again.")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /stats command to show statistics."""
        try:
            if not self.sheet_ops.is_connected():
                await update.message.reply_text(ERROR_SHEETS_API)
                return
            
            # Get command arguments for specific month
            command, args = extract_command_args(update.message.text)
            month = args.strip() if args else None
            
            success, message, stats = self.sheet_ops.get_monthly_stats(month)
            
            if success:
                await update.message.reply_text(
                    message,
                    parse_mode='Markdown'
                )
                month_display = month or "all time"
                logger.info(f"User {update.effective_user.id} requested stats for {month_display}")
            else:
                await update.message.reply_text(message)
                logger.warning(f"Failed to get stats for user {update.effective_user.id}")
                
        except Exception as e:
            logger.error(f"Error in stats command: {str(e)}")
            await update.message.reply_text("❌ Error getting statistics. Please try again.")
    
    async def recent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /recent command to show recent expenses."""
        try:
            if not self.sheet_ops.is_connected():
                await update.message.reply_text(ERROR_SHEETS_API)
                return
            
            # Get command arguments for number of recent expenses
            command, args = extract_command_args(update.message.text)
            try:
                limit = int(args.strip()) if args else 5
                limit = min(max(limit, 1), 20)  # Limit between 1 and 20
            except ValueError:
                limit = 5
            
            success, message, expenses = self.sheet_ops.get_recent_expenses(limit)
            
            if success:
                await update.message.reply_text(
                    message,
                    parse_mode='Markdown'
                )
                logger.info(f"User {update.effective_user.id} requested {limit} recent expenses")
            else:
                await update.message.reply_text(message)
                logger.warning(f"Failed to get recent expenses for user {update.effective_user.id}")
                
        except Exception as e:
            logger.error(f"Error in recent command: {str(e)}")
            await update.message.reply_text("❌ Error getting recent expenses. Please try again.")
    
    async def analyze_monthly_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /analyze_monthly command for AI-powered monthly analysis."""
        try:
            if not self.sheet_ops.is_connected():
                await update.message.reply_text(ERROR_SHEETS_API)
                return
            
            # Initialize AI analyzer if not already done
            if self.ai_analyzer is None:
                try:
                    self.ai_analyzer = MistralAnalyzer()
                    await update.message.reply_text("🤖 Initializing AI analyzer...")
                except Exception as e:
                    await update.message.reply_text(
                        "❌ Failed to initialize AI analyzer. Please ensure Ollama is running locally."
                    )
                    logger.error(f"Failed to initialize AI analyzer: {e}")
                    return
            
            # Send initial message
            await update.message.reply_text(
                "🔍 **Starting Monthly AI Analysis**\n\n"
                "This will take a few moments as the AI processes your data in stages:\n"
                "1️⃣ **Flow 1**: Categorizing expenses\n"
                "2️⃣ **Flow 2**: Analyzing patterns\n"
                "3️⃣ **Flow 3**: Generating insights\n\n"
                "⏳ Please wait..."
            )
            
            # Perform the analysis
            try:
                result = self.ai_analyzer.analyze_expenses('monthly')
                report = self.ai_analyzer.format_analysis_report(result)
                
                await update.message.reply_text(
                    report,
                    parse_mode='Markdown'
                )
                
                logger.info(f"User {update.effective_user.id} completed monthly AI analysis")
                
            except Exception as e:
                await update.message.reply_text(
                    f"❌ Error during AI analysis: {str(e)}\n\n"
                    "Please ensure Ollama is running and try again."
                )
                logger.error(f"AI analysis error for user {update.effective_user.id}: {e}")
                
        except Exception as e:
            logger.error(f"Error in analyze_monthly command: {str(e)}")
            await update.message.reply_text("❌ Error starting monthly analysis. Please try again.")
    
    async def analyze_annual_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /analyze_annual command for AI-powered annual analysis."""
        try:
            if not self.sheet_ops.is_connected():
                await update.message.reply_text(ERROR_SHEETS_API)
                return
            
            # Initialize AI analyzer if not already done
            if self.ai_analyzer is None:
                try:
                    self.ai_analyzer = MistralAnalyzer()
                    await update.message.reply_text("🤖 Initializing AI analyzer...")
                except Exception as e:
                    await update.message.reply_text(
                        "❌ Failed to initialize AI analyzer. Please ensure Ollama is running locally."
                    )
                    logger.error(f"Failed to initialize AI analyzer: {e}")
                    return
            
            # Send initial message
            await update.message.reply_text(
                "🔍 **Starting Annual AI Analysis**\n\n"
                "This will take a few moments as the AI processes your data in stages:\n"
                "1️⃣ **Flow 1**: Categorizing expenses\n"
                "2️⃣ **Flow 2**: Analyzing patterns\n"
                "3️⃣ **Flow 3**: Generating insights\n\n"
                "⏳ Please wait..."
            )
            
            # Perform the analysis
            try:
                result = self.ai_analyzer.analyze_expenses('annual')
                report = self.ai_analysis_report(result)
                
                await update.message.reply_text(
                    report,
                    parse_mode='Markdown'
                )
                
                logger.info(f"User {update.effective_user.id} completed annual AI analysis")
                
            except Exception as e:
                await update.message.reply_text(
                    f"❌ Error during AI analysis: {str(e)}\n\n"
                    "Please ensure Ollama is running and try again."
                )
                logger.error(f"AI analysis error for user {update.effective_user.id}: {e}")
                
        except Exception as e:
            logger.error(f"Error in analyze_annual command: {str(e)}")
            await update.message.reply_text("❌ Error starting annual analysis. Please try again.")
    
    async def monthly_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /monthly_report command with button options."""
        try:
            if not self.sheet_ops.is_connected():
                await update.message.reply_text(ERROR_SHEETS_API)
                return
            
            # Create inline keyboard with options
            keyboard = [
                [
                    InlineKeyboardButton("📊 Simple Total", callback_data="monthly_simple"),
                    InlineKeyboardButton("🤖 AI Analysis", callback_data="monthly_ai")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "📅 **Monthly Report Options**\n\n"
                "Choose how you'd like to view your monthly expenses:",
                reply_markup=reply_markup
            )
            
            logger.info(f"User {update.effective_user.id} requested monthly report options")
            
        except Exception as e:
            logger.error(f"Error in monthly_report command: {str(e)}")
            await update.message.reply_text("❌ Error showing monthly report options. Please try again.")
    
    async def annual_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /annual_report command with button options."""
        try:
            if not self.sheet_ops.is_connected():
                await update.message.reply_text(ERROR_SHEETS_API)
                return
            
            # Create inline keyboard with options
            keyboard = [
                [
                    InlineKeyboardButton("📊 Simple Total", callback_data="annual_simple"),
                    InlineKeyboardButton("🤖 AI Analysis", callback_data="annual_ai")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "📅 **Annual Report Options**\n\n"
                "Choose how you'd like to view your annual expenses:",
                reply_markup=reply_markup
            )
            
            logger.info(f"User {update.effective_user.id} requested annual report options")
            
        except Exception as e:
            logger.error(f"Error in annual_report command: {str(e)}")
            await update.message.reply_text("❌ Error showing annual report options. Please try again.")
    
    async def handle_button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks for report options."""
        try:
            query = update.callback_query
            await query.answer()  # Answer the callback query
            
            callback_data = query.data
            user_id = update.effective_user.id
            
            if callback_data == "monthly_simple":
                await self._handle_simple_monthly_report(query)
            elif callback_data == "monthly_ai":
                await self._handle_ai_monthly_report(query)
            elif callback_data == "annual_simple":
                await self._handle_simple_annual_report(query)
            elif callback_data == "annual_ai":
                await self._handle_ai_annual_report(query)
            else:
                await query.edit_message_text("❌ Unknown option selected.")
                
        except Exception as e:
            logger.error(f"Error handling button callback: {str(e)}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Error processing your selection. Please try again.")
    
    async def _handle_simple_monthly_report(self, query):
        """Handle simple monthly report request."""
        try:
            # Get monthly data and create simple report
            success, message, data = self.sheet_ops.get_monthly_stats("current")
            
            if success:
                await query.edit_message_text(
                    f"📊 **Monthly Report - Simple Total**\n\n{message}",
                    parse_mode='Markdown'
                )
                logger.info(f"User {query.from_user.id} viewed simple monthly report")
            else:
                await query.edit_message_text(f"❌ {message}")
                
        except Exception as e:
            logger.error(f"Error in simple monthly report: {e}")
            await query.edit_message_text("❌ Error generating monthly report. Please try again.")
    
    async def _handle_simple_annual_report(self, query):
        """Handle simple annual report request."""
        try:
            # Get annual data and create simple report
            success, message, data = self.sheet_ops.get_monthly_stats("annual")
            
            if success:
                await query.edit_message_text(
                    f"📊 **Annual Report - Simple Total**\n\n{message}",
                    parse_mode='Markdown'
                )
                logger.info(f"User {query.from_user.id} viewed simple annual report")
            else:
                await query.edit_message_text(f"❌ {message}")
                
        except Exception as e:
            logger.error(f"Error in simple annual report: {e}")
            await query.edit_message_text("❌ Error generating annual report. Please try again.")
    
    async def _handle_ai_monthly_report(self, query):
        """Handle AI monthly report request."""
        try:
            # Initialize AI analyzer if needed
            if self.ai_analyzer is None:
                try:
                    self.ai_analyzer = MistralAnalyzer()
                    await query.edit_message_text("🤖 Initializing AI analyzer...")
                except Exception as e:
                    await query.edit_message_text(
                        "❌ Failed to initialize AI analyzer. Please ensure Ollama is running locally."
                    )
                    logger.error(f"Failed to initialize AI analyzer: {e}")
                    return
            
            # Send initial message
            await query.edit_message_text(
                "🔍 **Starting Monthly AI Analysis**\n\n"
                "This will take a few moments as the AI processes your data in stages:\n"
                "1️⃣ **Flow 1**: Categorizing expenses\n"
                "2️⃣ **Flow 2**: Analyzing patterns\n"
                "3️⃣ **Flow 3**: Generating insights\n\n"
                "⏳ Please wait..."
            )
            
            # Perform the analysis
            try:
                result = self.ai_analyzer.analyze_expenses('monthly')
                report = self.ai_analyzer.format_analysis_report(result)
                
                # Log the AI analysis to sheets
                await self._log_ai_analysis_to_sheets('monthly', result)
                
                await query.edit_message_text(
                    report,
                    parse_mode='Markdown'
                )
                
                logger.info(f"User {query.from_user.id} completed monthly AI analysis")
                
            except Exception as e:
                await query.edit_message_text(
                    f"❌ Error during AI analysis: {str(e)}\n\n"
                    "Please ensure Ollama is running and try again."
                )
                logger.error(f"AI analysis error for user {query.from_user.id}: {e}")
                
        except Exception as e:
            logger.error(f"Error in AI monthly report: {e}")
            await query.edit_message_text("❌ Error starting monthly AI analysis. Please try again.")
    
    async def _handle_ai_annual_report(self, query):
        """Handle AI annual report request."""
        try:
            # Initialize AI analyzer if needed
            if self.ai_analyzer is None:
                try:
                    self.ai_analyzer = MistralAnalyzer()
                    await query.edit_message_text("🤖 Initializing AI analyzer...")
                except Exception as e:
                    await query.edit_message_text(
                        "❌ Failed to initialize AI analyzer. Please ensure Ollama is running locally."
                    )
                    logger.error(f"Failed to initialize AI analyzer: {e}")
                    return
            
            # Send initial message
            await query.edit_message_text(
                "🔍 **Starting Annual AI Analysis**\n\n"
                "This will take a few moments as the AI processes your data in stages:\n"
                "1️⃣ **Flow 1**: Categorizing expenses\n"
                "2️⃣ **Flow 2**: Analyzing patterns\n"
                "3️⃣ **Flow 3**: Generating insights\n\n"
                "⏳ Please wait..."
            )
            
            # Perform the analysis
            try:
                result = self.ai_analyzer.analyze_expenses('annual')
                report = self.ai_analyzer.format_analysis_report(result)
                
                # Log the AI analysis to sheets
                await self._log_ai_analysis_to_sheets('annual', result)
                
                await query.edit_message_text(
                    report,
                    parse_mode='Markdown'
                )
                
                logger.info(f"User {query.from_user.id} completed annual AI analysis")
                
            except Exception as e:
                await query.edit_message_text(
                    f"❌ Error during AI analysis: {str(e)}\n\n"
                    "Please ensure Ollama is running and try again."
                )
                logger.error(f"AI analysis error for user {query.from_user.id}: {e}")
                
        except Exception as e:
            logger.error(f"Error in AI annual report: {e}")
            await query.edit_message_text("❌ Error starting annual AI analysis. Please try again.")
    
    async def _log_ai_analysis_to_sheets(self, period: str, result):
        """Log AI analysis results to Google Sheets."""
        try:
            # Create analysis log entry
            analysis_data = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'time': datetime.now().strftime("%H:%M:%S"),
                'period': period,
                'total_expenses': result.total_expenses,
                'total_transactions': result.total_transactions,
                'categories_count': len(result.categories),
                'insights_count': len(result.insights),
                'recommendations_count': len(result.recommendations),
                'analysis_date': result.analysis_date
            }
            
            # Log to sheets (this will need to be implemented in SheetOperations)
            success = self.sheet_ops.log_ai_analysis(analysis_data)
            
            if success:
                logger.info(f"AI analysis logged to sheets for {period} period")
            else:
                logger.warning(f"Failed to log AI analysis to sheets for {period} period")
                
        except Exception as e:
            logger.error(f"Error logging AI analysis to sheets: {e}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages for expense logging."""
        try:
            message_text = update.message.text.strip()
            user_id = update.effective_user.id
            
            # Skip if it's a command
            if is_command(message_text):
                return
            
            # Check if sheets are connected
            if not self.sheet_ops.is_connected():
                await update.message.reply_text(ERROR_SHEETS_API)
                return
            
            # Parse the expense message
            amount, category, error_msg = parse_expense_message(message_text)
            
            if error_msg:
                # Send error message with suggestions
                suggestions = format_category_suggestions()
                full_error = f"{error_msg}\n\n{suggestions}"
                await update.message.reply_text(full_error)
                logger.warning(f"User {user_id} sent invalid message: {message_text}")
                return
            
            # Validate the parsed data
            if not amount or not category:
                await update.message.reply_text(ERROR_INVALID_FORMAT)
                return
            
            # Log the expense
            success, response_msg, total = self.sheet_ops.log_expense(amount, category)
            
            if success:
                await update.message.reply_text(response_msg)
                logger.info(f"User {user_id} logged expense: ${amount} for {category}")
                
                # Add category suggestions for future use
                if total > 0:
                    suggestions = format_category_suggestions()
                    await update.message.reply_text(suggestions)
            else:
                await update.message.reply_text(response_msg)
                logger.error(f"Failed to log expense for user {user_id}: ${amount} for {category}")
                
        except Exception as e:
            logger.error(f"Error handling message from user {update.effective_user.id}: {str(e)}")
            await update.message.reply_text("❌ Error processing your message. Please try again.")
    
    async def error_handler(self, update: Union[Update, None], context: ContextTypes.DEFAULT_TYPE):
        """Handle errors in the bot."""
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ An error occurred while processing your request. Please try again later."
                )
            
            logger.error(f"Exception while handling an update: {context.error}")
            
        except Exception as e:
            logger.error(f"Error in error handler: {str(e)}")
    
    def get_command_handlers(self):
        """Get a list of command handlers for registration."""
        return [
            ('start', self.start_command),
            ('help', self.help_command),
            ('total', self.total_command),
            ('stats', self.stats_command),
            ('recent', self.recent_command),
            ('analyze_monthly', self.analyze_monthly_command),
            ('analyze_annual', self.analyze_annual_command),
            ('monthly_report', self.monthly_report_command),
            ('annual_report', self.annual_report_command),
        ]
    
    def get_callback_query_handler(self):
        """Get the callback query handler for button interactions."""
        return self.handle_button_callback
    
    def get_message_handler(self):
        """Get the message handler for registration."""
        return self.handle_message
    
    def get_error_handler(self):
        """Get the error handler for registration."""
        return self.error_handler
