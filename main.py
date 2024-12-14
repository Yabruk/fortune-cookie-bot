import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from random import choice
from flask import Flask

# Отримуємо токен із змінного середовища
TOKEN = os.getenv('BOT_TOKEN')

# Список передбачень
FORTUNES = [
    "Сьогодні твій щасливий день!",
    "Час почати щось нове та вірити у себе.",
    "Тебе чекає приємний сюрприз.",
    "Скоро ти отримаєш добру новину.",
    "Не бійся змін – вони принесуть користь.",
]

# Flask додаток для запуску на Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

# Асинхронна функція для команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Створюємо меню у вигляді клавіатури
    keyboard = [["Отримати передбачення", "Допомога"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Привіт! Обери опцію нижче:",
        reply_markup=reply_markup
    )

# Асинхронна функція для відповіді на вибір "Отримати передбачення"
async def send_fortune(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(choice(FORTUNES))

# Асинхронна функція для відповіді на вибір "Допомога"
async def help_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Натисни 'Отримати передбачення', щоб дізнатися свою долю! "
        "Або використай /start, щоб оновити меню."
    )

# Обробник текстових повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()

    if "передбачення" in user_message:
        await send_fortune(update, context)
    elif "допомога" in user_message:
        await help_message(update, context)
    else:
        await update.message.reply_text("Вибери опцію з меню!")

def main() -> None:
    # Створюємо додаток з токеном
    application = Application.builder().token(TOKEN).build()

    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаємо polling для Telegram бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Flask сервер слухає на порту, який визначається змінною середовища PORT
if __name__ == '__main__':
    from threading import Thread

    # Запускаємо Flask сервер у фоновому потоці
    def run_flask():
        app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

    # Стартуємо Flask сервер
    thread = Thread(target=run_flask)
    thread.start()

    # Запускаємо Telegram бота
    main()
