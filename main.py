import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Отримуємо токен із змінної оточення
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Список передбачень
FORTUNES = [
    "Сьогодні твій день! 😎",
    "Очікуй приємний сюрприз найближчим часом! 🎉",
    "Твоя енергія привертає успіх! 🚀",
    "Зустрінеш старого друга, який змінить твій настрій! 😊",
    "Час для відпочинку. Твоє тіло скаже тобі дякую! 🧘‍♀️",
    "Важливе рішення прийде легко! 🧠",
    "Будь готовий до несподіваних новин! 📬",
    "Зроби крок вперед – успіх не за горами! 🏞️"
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Привітальне повідомлення зі стартовою кнопкою."""
    keyboard = [[InlineKeyboardButton("Отримати передбачення 🍪", callback_data='get_fortune')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привіт! 🥳 Натисни кнопку нижче, щоб отримати своє передбачення 🍪.",
        reply_markup=reply_markup
    )

# Обробка натискання кнопки "Отримати передбачення 🍪"
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Вибір випадкового передбачення."""
    query = update.callback_query
    await query.answer()  # Підтверджуємо натискання кнопки
    random_fortune = random.choice(FORTUNES)
    await query.edit_message_text(f"Твоє передбачення: \n\n🔮 *{random_fortune}* 🔮", parse_mode='Markdown')

# Основна точка запуску
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обробники
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button_click))

    print("Бот запущено 🔥")
    app.run_polling()
