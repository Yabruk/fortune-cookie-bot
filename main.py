import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Отримуємо змінні з оточення
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL твого бота
PORT = int(os.getenv("PORT", "8443"))  # Render автоматично створює змінну PORT

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Отримати передбачення 🍪", callback_data='get_fortune')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привіт! Натисни кнопку нижче, щоб отримати своє передбачення 🍪.",
        reply_markup=reply_markup
    )

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    fortune = random.choice(FORTUNES)
    await query.edit_message_text(f"🔮 *{fortune}* 🔮", parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button_click))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=f"/{BOT_TOKEN}"  # URL шляху для вебхука
    )
    app.bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")  # Встановлення вебхука
