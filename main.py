import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Список передбачень
FORTUNES = [
    "Сьогодні твій день, скористайся ним!",
    "Твоя робота буде оцінена.",
    "Не бійся змін, вони принесуть успіх.",
    "Прийми нові можливості з відкритим серцем.",
    "Твоя удача зовсім близько!",
    "Вір у себе – і все вдасться.",
]

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Користувач {update.effective_user.username} виконав /start")
    keyboard = [[InlineKeyboardButton("Передбачення", callback_data="get_fortune")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Вітаю! Натисни кнопку, щоб отримати передбачення:", reply_markup=reply_markup)

# Обробник натискання кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "get_fortune":
        fortune = FORTUNES.pop(0)
        FORTUNES.append(fortune)
        await query.edit_message_text(f"✨ Твоє передбачення: {fortune}")
    logging.info(f"Користувач {update.effective_user.username} натиснув кнопку")

# Головна функція
def main():
    try:
        logging.info("🔄 Запуск програми...")
        token = os.getenv("BOT_TOKEN")
        if not token:
            raise ValueError("❌ BOT_TOKEN не знайдено у змінних середовища.")

        # Отримання URL та порту для Webhook
        webhook_url = os.getenv("RENDER_EXTERNAL_URL", "") + "/webhook"
        port = int(os.getenv("PORT", 8443))

        logging.info(f"🌐 Порт: {port}")
        logging.info(f"🔗 Webhook URL: {webhook_url}")

        # Створення застосунку
        application = ApplicationBuilder().token(token).build()

        # Додавання обробників
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))

        # Запуск Webhook
        logging.info("🚀 Запуск Webhook...")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=webhook_url,
        )
    except Exception as e:
        logging.error(f"❌ Помилка: {e}")

if __name__ == "__main__":
    main()
