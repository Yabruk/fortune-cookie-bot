import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from random import choice
import asyncio

# Отримуємо токен із змінного середовища
TOKEN = os.getenv('BOT_TOKEN')
APP_URL = os.getenv('APP_URL')  # URL вашого додатка на Render

# Список передбачень
FORTUNES = [
    "Сьогодні твій щасливий день!",
    "ВЕБ ХУУУУК",
    "Час почати щось нове та вірити у себе.",
    "Тебе чекає приємний сюрприз.",
    "Скоро ти отримаєш добру новину.",
    "Не бійся змін – вони принесуть користь.",
]

# Ініціалізація Flask-додатка
app = Flask(__name__)

# Ініціалізація Telegram Application
application = ApplicationBuilder().token(TOKEN).build()

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привіт! Натисни /fortune, щоб отримати своє передбачення!')

# Обробник команди /fortune
async def fortune(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(choice(FORTUNES))

# Додаємо обробники команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("fortune", fortune))

@app.route('/')
def home():
    return "Бот працює! Вебхук налаштовано правильно.", 200

@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    """ Основна точка прийому оновлень від Telegram """
    try:
        data = request.get_json(force=True)
        print("Отримано дані від Telegram:", data)  # Логування
        update = Update.de_json(data, application.bot)
        print("Декодоване оновлення:", update)  # Логування оновлення
        application.update_queue.put_nowait(update)
        print("Оновлення додано до черги.")
    except Exception as e:
        print("Помилка обробки вебхука:", e)  # Лог помилки
    return 'ok', 200

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook() -> str:
    """ Встановлює вебхук при першому запуску додатку """
    webhook_url = f"{APP_URL}/webhook"
    try:
        asyncio.run(application.bot.set_webhook(webhook_url))
        return f"Webhook встановлено: {webhook_url}", 200
    except Exception as e:
        return f"Помилка встановлення вебхука: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
