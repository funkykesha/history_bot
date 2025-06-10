import unittest
from unittest.mock import Mock, patch
from datetime import datetime
import os
from src.utils.exporters.chat_exporter import ChatExporter
from src.config import EXPORT_DIR, MAX_EXPORT_AGE_DAYS

class TestChatExporter(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.exporter = ChatExporter(self.bot)
        self.test_username = "test_user"
        self.test_user_id = 123456789

    def tearDown(self):
        # Clean up test files
        if os.path.exists(EXPORT_DIR):
            for file in os.listdir(EXPORT_DIR):
                os.remove(os.path.join(EXPORT_DIR, file))

    @patch('src.utils.exporters.chat_exporter.ChatExporter._get_user_info')
    def test_export_chat_success(self, mock_get_user_info):
        # Mock user info
        mock_get_user_info.return_value = {
            'id': self.test_user_id,
            'username': self.test_username
        }

        # Mock messages
        self.bot.get_chat_history.return_value = [
            Mock(
                id=1,
                date=datetime.now(),
                text="Test message 1",
                from_user=Mock(username=self.test_username)
            ),
            Mock(
                id=2,
                date=datetime.now(),
                text="Test message 2",
                from_user=Mock(username=self.test_username)
            )
        ]

        # Test export
        result = self.exporter.export_chat(self.test_username)
        
        # Verify results
        self.assertTrue(result['success'])
        self.assertTrue(os.path.exists(result['file_path']))
        self.assertIn(self.test_username, result['file_path'])
        
        # Verify file contents
        with open(result['file_path'], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test message 1", content)
            self.assertIn("Test message 2", content)

    @patch('src.utils.exporters.chat_exporter.ChatExporter._get_user_info')
    def test_export_chat_no_messages(self, mock_get_user_info):
        # Mock user info
        mock_get_user_info.return_value = {
            'id': self.test_user_id,
            'username': self.test_username
        }

        # Mock empty messages
        self.bot.get_chat_history.return_value = []

        # Test export
        result = self.exporter.export_chat(self.test_username)
        
        # Verify results
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "No messages found")

    def test_export_chat_invalid_username(self):
        # Test with invalid username
        result = self.exporter.export_chat("invalid_user")
        
        # Verify results
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "User not found")

    def test_cleanup_old_exports(self):
        # Create test files with different ages
        os.makedirs(EXPORT_DIR, exist_ok=True)
        
        # Create a new file
        new_file = os.path.join(EXPORT_DIR, f"new_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(new_file, 'w') as f:
            f.write("New file content")

        # Create an old file
        old_file = os.path.join(EXPORT_DIR, f"old_export_20200101_000000.txt")
        with open(old_file, 'w') as f:
            f.write("Old file content")

        # Run cleanup
        self.exporter.cleanup_old_exports()

        # Verify results
        self.assertTrue(os.path.exists(new_file))
        self.assertFalse(os.path.exists(old_file))

if __name__ == '__main__':
    unittest.main() 