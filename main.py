import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привіт! Натисни /fortune, щоб отримати своє передбачення!')

# Обробник команди /fortune
async def fortune(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from random import choice
    await update.message.reply_text(choice(FORTUNES))

# Створюємо інстанс Application для роботи з вебхуками
application = ApplicationBuilder().token(TOKEN).build()

# Додаємо обробники команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("fortune", fortune))

@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    """ Основна точка прийому оновлень від Telegram """
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return 'ok', 200

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook() -> str:
    """ Встановлює вебхук при першому запуску додатку """
    webhook_url = f"{APP_URL}/webhook"
    success = application.bot.set_webhook(webhook_url)
    if success:
        return f"Webhook встановлено: {webhook_url}", 200
    else:
        return "Помилка встановлення вебхука", 500

if __name__ == '__main__':
    # Запускаємо Flask-додаток
    app.run(host='0.0.0.0', port=5000)
