import logging
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import os
from src.utils.exporters.chat_exporter import ChatExporter

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"User {user.id} started the bot")
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        "Я бот для экспорта истории чатов. Вот что я умею:\n\n"
        "📝 /export <username> - Экспортировать историю чата\n"
        "❓ /help - Показать это сообщение\n\n"
        "Просто отправь мне команду /export и имя пользователя, "
        "и я отправлю тебе файл с историей переписки."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "📚 Доступные команды:\n\n"
        "📝 /export <username> - Экспортировать историю чата с указанным пользователем\n"
        "❓ /help - Показать это сообщение\n\n"
        "Пример использования:\n"
        "/export username\n\n"
        "Бот отправит вам текстовый файл с историей переписки, "
        "включая даты и время сообщений."
    )

async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /export command."""
    if not context.args:
        await update.message.reply_text(
            "❌ Пожалуйста, укажите имя пользователя.\n"
            "Пример: /export username"
        )
        return

    username = context.args[0].lstrip('@')
    user = update.effective_user
    
    try:
        # Send initial response
        status_message = await update.message.reply_text(
            f"⏳ Начинаю экспорт чата с @{username}...\n"
            "Это может занять некоторое время."
        )
        
        # Get chat exporter from context
        chat_exporter = context.bot_data.get('chat_exporter')
        if not chat_exporter:
            chat_exporter = ChatExporter(context.bot)
            context.bot_data['chat_exporter'] = chat_exporter
        
        # Export chat
        filepath = await chat_exporter.export_chat(user.id, username)
        
        if filepath and os.path.exists(filepath):
            # Send the file
            with open(filepath, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename=os.path.basename(filepath),
                    caption=f"✅ Экспорт чата с @{username} завершен!"
                )
            
            # Clean up the file
            os.remove(filepath)
            
            # Update status message
            await status_message.delete()
        else:
            await status_message.edit_text(
                f"❌ Не удалось экспортировать чат с @{username}.\n"
                "Убедитесь, что:\n"
                "1. Пользователь существует\n"
                "2. У вас есть общая история переписки\n"
                "3. Пользователь не заблокировал бота"
            )
        
    except Exception as e:
        logger.error(f"Error during export for user {user.id}: {str(e)}")
        await update.message.reply_text(
            "❌ Произошла ошибка при экспорте чата.\n"
            "Пожалуйста, попробуйте позже."
        ) 