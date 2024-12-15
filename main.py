import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
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
    # Створюємо меню з кнопками
    keyboard = [
        [InlineKeyboardButton("Отримати передбачення", callback_data="get_fortune")],
        [InlineKeyboardButton("Допомога", callback_data="help_message")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Відправляємо меню без тексту (використовуємо невидимий символ)
    await update.message.reply_text(".", reply_markup=reply_markup)

# Асинхронна функція для обробки кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Підтверджуємо отримання callback'у

    if query.data == "get_fortune":
        # Відправляємо передбачення
        await query.edit_message_text(choice(FORTUNES))
    elif query.data == "help_message":
        # Відправляємо допомогу
        await query.edit_message_text(
            "Натисни 'Отримати передбачення', щоб дізнатися свою долю! "
            "Або використай /start, щоб оновити меню."
        )

def main() -> None:
    # Створюємо додаток з токеном
    application = Application.builder().token(TOKEN).build()

    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

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
