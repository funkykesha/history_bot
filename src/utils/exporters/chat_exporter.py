import logging
from datetime import datetime
from telegram import Bot, User
from telegram.error import TelegramError, BadRequest
import os
from typing import List, Optional, Dict
import asyncio

logger = logging.getLogger(__name__)

class ChatExporter:
    def __init__(self, bot: Bot, export_dir: str = "exports"):
        self.bot = bot
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)

    async def get_user_info(self, username: str) -> Optional[User]:
        """Get user information by username."""
        try:
            # Try to get user by username
            chat = await self.bot.get_chat(f"@{username}")
            return chat
        except BadRequest as e:
            logger.error(f"Error getting user info for {username}: {str(e)}")
            return None

    async def export_chat(self, user_id: int, target_username: str) -> Optional[str]:
        """
        Export chat history with a specific user.
        
        Args:
            user_id: The ID of the user requesting the export
            target_username: The username of the target user
            
        Returns:
            Optional[str]: Path to the exported file if successful, None otherwise
        """
        try:
            # Get target user info
            target_user = await self.get_user_info(target_username)
            if not target_user:
                logger.error(f"Could not find user: {target_username}")
                return None

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_{target_username}_{timestamp}.txt"
            filepath = os.path.join(self.export_dir, filename)
            
            # Get chat history
            messages = []
            async for message in self.bot.get_chat_history(chat_id=target_user.id, limit=1000):
                if message.text:  # Only export text messages for now
                    messages.append({
                        'date': message.date,
                        'from_user': message.from_user.full_name if message.from_user else 'Unknown',
                        'text': message.text
                    })

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Chat history with @{target_username}\n")
                f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for msg in messages:
                    f.write(f"[{msg['date'].strftime('%Y-%m-%d %H:%M:%S')}] {msg['from_user']}:\n")
                    f.write(f"{msg['text']}\n\n")
                
                f.write("\n" + "=" * 50 + "\n")
                f.write(f"Total messages: {len(messages)}\n")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting chat for user {user_id}: {str(e)}")
            return None

    async def cleanup_old_exports(self, max_age_hours: int = 24) -> None:
        """
        Clean up old export files.
        
        Args:
            max_age_hours: Maximum age of export files in hours
        """
        try:
            current_time = datetime.now()
            for filename in os.listdir(self.export_dir):
                filepath = os.path.join(self.export_dir, filename)
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                age_hours = (current_time - file_time).total_seconds() / 3600
                
                if age_hours > max_age_hours:
                    os.remove(filepath)
                    logger.info(f"Removed old export file: {filename}")
                    
        except Exception as e:
            logger.error(f"Error cleaning up old exports: {str(e)}") 