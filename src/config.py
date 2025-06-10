import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')

# Export Configuration
EXPORT_DIR = os.getenv('EXPORT_DIR', 'exports')
MAX_EXPORT_SIZE = int(os.getenv('MAX_EXPORT_SIZE', '1000'))  # Maximum messages to export
RATE_LIMIT = int(os.getenv('RATE_LIMIT', '5'))  # Exports per hour per user

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/bot.log')

# Create necessary directories
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs('logs', exist_ok=True) 