import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from src.config import BOT_TOKEN, LOG_LEVEL, LOG_FILE, EXPORT_DIR
from src.bot.handlers.command_handlers import start_command, help_command, export_command
from src.utils.exporters.chat_exporter import ChatExporter

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL),
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def error_handler(update, context):
    """Log the error and send a message to the user."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            'Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.'
        )

async def main():
    """Start the bot."""
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Initialize chat exporter
        chat_exporter = ChatExporter(application.bot, EXPORT_DIR)
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("export", export_command))
        
        # Add error handler
        application.add_error_handler(error_handler)

        # Start the Bot
        logger.info("Starting bot...")
        await application.initialize()
        await application.start()
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        raise
    finally:
        if 'application' in locals():
            await application.stop()
            await application.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True) 