#!/usr/bin/env python3
"""
Main entry point for the Telegram Expense Logging Bot.
"""
import asyncio
import logging
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot.handlers import BotHandlers
from config.settings import TELEGRAM_BOT_TOKEN, LOG_LEVEL
from sheets.operations import SheetOperations

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL.upper()),
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to run the bot."""
    try:
        logger.info("Starting Telegram Expense Logging Bot...")
        
        # Test Google Sheets connection via Apps Script
        logger.info("Testing Google Sheets connection...")
        try:
            sheet_ops = SheetOperations()
            if sheet_ops.is_connected():
                logger.info("✅ Google Sheets connection successful")
                
                # Log connection info
                conn_info = sheet_ops.get_connection_info()
                logger.info(f"Connected to spreadsheet: {conn_info['spreadsheet_id']}")
                logger.info(f"Web App URL: {conn_info['webapp_url']}")
            else:
                logger.error("❌ Google Sheets connection failed")
                sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Failed to initialize Google Sheets: {str(e)}")
            sys.exit(1)
        
        # Create the Application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Initialize handlers
        handlers = BotHandlers()
        
        # Add command handlers
        for command, handler_func in handlers.get_command_handlers():
            application.add_handler(CommandHandler(command, handler_func))
            logger.info(f"Registered command handler: /{command}")
        
        # Add callback query handler for button interactions
        application.add_handler(
            CallbackQueryHandler(handlers.get_callback_query_handler())
        )
        logger.info("Registered callback query handler for button interactions")
        
        # Add message handler for expense logging
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_message_handler())
        )
        logger.info("Registered message handler for expense logging")
        
        # Add error handler
        application.add_error_handler(handlers.get_error_handler())
        logger.info("Registered error handler")
        
        # Start the bot
        logger.info("Starting bot...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        
        # Keep the bot running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Received stop signal, shutting down...")
        finally:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
            logger.info("Bot stopped successfully.")
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
