import unittest
from unittest.mock import Mock, patch
from telegram import Update, User, Message, Chat
from telegram.ext import CallbackContext
from src.bot.handlers.command_handlers import (
    start_command,
    help_command,
    export_command
)

class TestCommandHandlers(unittest.TestCase):
    def setUp(self):
        self.user = User(
            id=123456789,
            first_name="Test",
            is_bot=False,
            username="test_user"
        )
        self.chat = Chat(
            id=123456789,
            type="private"
        )
        self.message = Message(
            message_id=1,
            date=None,
            chat=self.chat,
            from_user=self.user
        )
        self.update = Update(
            update_id=1,
            message=self.message
        )
        self.context = CallbackContext(Mock())

    @patch('src.bot.handlers.command_handlers.logger')
    def test_start_command(self, mock_logger):
        # Test start command
        start_command(self.update, self.context)
        
        # Verify message was sent
        self.context.bot.send_message.assert_called_once()
        call_args = self.context.bot.send_message.call_args[1]
        self.assertEqual(call_args['chat_id'], self.chat.id)
        self.assertIn("Welcome", call_args['text'])

    @patch('src.bot.handlers.command_handlers.logger')
    def test_help_command(self, mock_logger):
        # Test help command
        help_command(self.update, self.context)
        
        # Verify message was sent
        self.context.bot.send_message.assert_called_once()
        call_args = self.context.bot.send_message.call_args[1]
        self.assertEqual(call_args['chat_id'], self.chat.id)
        self.assertIn("Available commands", call_args['text'])

    @patch('src.bot.handlers.command_handlers.ChatExporter')
    @patch('src.bot.handlers.command_handlers.logger')
    def test_export_command_success(self, mock_logger, mock_exporter):
        # Mock exporter
        mock_exporter_instance = Mock()
        mock_exporter.return_value = mock_exporter_instance
        mock_exporter_instance.export_chat.return_value = {
            'success': True,
            'file_path': 'test_export.txt'
        }

        # Set command arguments
        self.update.message.text = "/export test_user"

        # Test export command
        export_command(self.update, self.context)
        
        # Verify exporter was called
        mock_exporter_instance.export_chat.assert_called_once_with("test_user")
        
        # Verify file was sent
        self.context.bot.send_document.assert_called_once()
        call_args = self.context.bot.send_document.call_args[1]
        self.assertEqual(call_args['chat_id'], self.chat.id)
        self.assertEqual(call_args['document'], 'test_export.txt')

    @patch('src.bot.handlers.command_handlers.ChatExporter')
    @patch('src.bot.handlers.command_handlers.logger')
    def test_export_command_no_username(self, mock_logger, mock_exporter):
        # Set command without username
        self.update.message.text = "/export"

        # Test export command
        export_command(self.update, self.context)
        
        # Verify error message was sent
        self.context.bot.send_message.assert_called_once()
        call_args = self.context.bot.send_message.call_args[1]
        self.assertEqual(call_args['chat_id'], self.chat.id)
        self.assertIn("Please provide a username", call_args['text'])

    @patch('src.bot.handlers.command_handlers.ChatExporter')
    @patch('src.bot.handlers.command_handlers.logger')
    def test_export_command_error(self, mock_logger, mock_exporter):
        # Mock exporter
        mock_exporter_instance = Mock()
        mock_exporter.return_value = mock_exporter_instance
        mock_exporter_instance.export_chat.return_value = {
            'success': False,
            'error': 'Test error'
        }

        # Set command arguments
        self.update.message.text = "/export test_user"

        # Test export command
        export_command(self.update, self.context)
        
        # Verify error message was sent
        self.context.bot.send_message.assert_called_once()
        call_args = self.context.bot.send_message.call_args[1]
        self.assertEqual(call_args['chat_id'], self.chat.id)
        self.assertIn("Test error", call_args['text'])

if __name__ == '__main__':
    unittest.main() 