import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

# Отримуємо токен із змінного середовища
TOKEN = os.getenv('BOT_TOKEN')
APP_URL = os.getenv('APP_URL')  # URL вашого додатка на Render

# Список передбачень
FORTUNES = [
    "Сьогодні твій щасливий день!",
    "Час почати щось нове та вірити у себе.",
    "Тебе чекає приємний сюрприз.",
    "Скоро ти отримаєш добру новину.",
    "Не бійся змін – вони принесуть користь.",
]

# Ініціалізація Flask-додатка
app = Flask(__name__)

# Ініціалізація Telegram Bot і Dispatcher
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)  # Вебхук не потребує окремої черги

# Обробник команди /start
def start(update: Update, context) -> None:
    update.message.reply_text('Привіт! Натисни /fortune, щоб отримати своє передбачення!')

# Обробник команди /fortune
def fortune(update: Update, context) -> None:
    from random import choice
    update.message.reply_text(choice(FORTUNES))

# Додаємо обробники команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("fortune", fortune))

@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    """ Основна точка прийому оновлень від Telegram """
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok', 200

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook() -> str:
    """ Встановлює вебхук при першому запуску додатку """
    webhook_url = f"{APP_URL}/webhook"
    success = bot.set_webhook(webhook_url)
    if success:
        return f"Webhook встановлено: {webhook_url}", 200
    else:
        return "Помилка встановлення вебхука", 500

if __name__ == '__main__':
    # Запускаємо Flask-додаток
    app.run(host='0.0.0.0', port=5000)
