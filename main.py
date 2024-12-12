import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Отримуємо змінні з оточення
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "8443"))

# Перевірка URL
if not WEBHOOK_URL or not WEBHOOK_URL.startswith("https://"):
    raise ValueError("WEBHOOK_URL має бути задано та починатися з https://")

# Список передбачень
FORTUNES = [
    "Сьогодні твій день! 😎",
    "Очікуй приємний сюрприз найближчим часом! 🎉",
    "Твоя енергія привертає успіх! 🚀",
    "Зустрінеш старого друга, який змінить твій настрій! 😊",
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

    # Лог для перевірки
    print(f"Встановлюємо вебхук на: {WEBHOOK_URL}/webhook")

    # Запускаємо веб-сервер
    try:
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="/webhook"  # Шлях для обробки
        )
        success = app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")  # Установка вебхука
        print(f"Результат установки вебхука: {success}")
    except Exception as e:
        print(f"Помилка при встановленні вебхука: {e}")
        raise
