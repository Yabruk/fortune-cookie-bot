import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Установлюємо логування
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

# Функція старту
async def start(update: Update, context):
    logging.info(f"Користувач {update.effective_user.username} виконав /start")
    keyboard = [[InlineKeyboardButton("Передбачення", callback_data="get_fortune")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Вітаю! Натисни кнопку, щоб отримати передбачення:", reply_markup=reply_markup)

# Обробник кнопки
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()  # Закриває "годинник" на кнопці
    if query.data == "get_fortune":
        fortune = random.choice(FORTUNES)
        await query.edit_message_text(f"✨ Твоє передбачення: {fortune}")
    logging.info(f"Користувач {update.effective_user.username} натиснув кнопку")

# Головна функція
def main():
    try:
        logging.info("🔄 Запуск програми...")  # Лог на самому початку
        token = os.getenv("BOT_TOKEN")  # Токен отримується зі змінної середовища
        if not token:
            raise ValueError("❌ BOT_TOKEN не знайдено у змінних середовища.")

        # URL для Webhook
        port = int(os.getenv("PORT", 10000))  # Render надає порт через змінну середовища PORT
        webhook_url = os.getenv("RENDER_EXTERNAL_URL", "https://localhost") + "/webhook"

        logging.info(f"🌐 Порт: {port}")
        logging.info(f"🔗 Webhook URL: {webhook_url}")

        # Створення бота
        application = ApplicationBuilder().token(token).build()

        # Додавання обробників
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))

        logging.info("🚀 Запуск Webhook...")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=webhook_url,
        )
    except Exception as e:
        logging.error(f"❌ Помилка під час запуску програми: {e}")

if __name__ == "__main__":
    logging.info("🔄 Запускаємо основний процес...")
    main()
