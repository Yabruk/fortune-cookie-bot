import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request

# Список передбачень для "печива"
fortunes = [
    "Твоя удача сьогодні в руках!",
    "Завтра принесе нові можливості.",
    "Не бійтеся змін – вони на краще.",
    "Нехай ваш шлях буде легким і ясним.",
    "Ваші мрії скоро збудуться!",
    "Сьогодні - день великих досягнень!",
    "Ваша мудрість допоможе знайти правильний шлях.",
    "Не зупиняйтесь, якщо сьогодні не все йде за планом."
]

# Функція для видачі передбачення
async def fortune_cookie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    fortune = random.choice(fortunes)
    await update.message.reply_text(f"Ваше передбачення: {fortune}")

# Створення Flask додатку для Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def main():
    # Отримуємо токен з змінної середовища
    token = os.getenv('BOT_TOKEN')

    if not token:
        print("Токен не знайдено! Перевірте змінну середовища BOT_TOKEN.")
        return

    # Створення додатку для Telegram бота
    application = Application.builder().token(token).build()

    # Обробник команд
    application.add_handler(CommandHandler("fortune", fortune_cookie))

    # Запуск бота у фоновому режимі
    application.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    # Запускаємо Flask сервер
    from threading import Thread

    def run_flask():
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

    # Запускаємо Flask у фоновому режимі
    thread = Thread(target=run_flask)
    thread.start()

    # Запускаємо основний Telegram бот
    main()
