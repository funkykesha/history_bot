# Telegram Chat History Export Bot

Бот для экспорта истории чатов в текстовый файл.

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd telegram-chat-export-bot
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории:
```
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=sqlite:///bot.db
EXPORT_DIR=exports
MAX_EXPORT_SIZE=1000
RATE_LIMIT=5
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

## Запуск

```bash
python src/main.py
```

## Использование

1. Найдите бота в Telegram по его username
2. Отправьте команду /start для начала работы
3. Используйте /export <username> для экспорта истории чата
4. Бот отправит вам текстовый файл с историей переписки

## Команды

- /start - Начать работу с ботом
- /help - Показать список команд
- /export <username> - Экспортировать историю чата

## Разработка

### Структура проекта
```
src/
  ├── bot/          # Код бота
  ├── utils/        # Утилиты
  ├── database/     # Работа с БД
  └── main.py       # Точка входа
```

### Тестирование
```bash
pytest
```

## Лицензия

MIT 