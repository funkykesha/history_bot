import logging
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, LOG_LEVEL, LOG_FILE

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

async def start(update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Привет! Я бот для экспорта истории чатов. '
        'Используйте /export <username> чтобы получить историю переписки.'
    )

async def help_command(update, context):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        'Доступные команды:\n'
        '/start - Начать работу с ботом\n'
        '/help - Показать это сообщение\n'
        '/export <username> - Экспортировать историю чата с указанным пользователем'
    )

async def error_handler(update, context):
    """Log the error and send a message to the user."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            'Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.'
        )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main() 