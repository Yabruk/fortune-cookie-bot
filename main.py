import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

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
    print(f"Користувач {update.effective_user.username} виконав /start")
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
    print(f"Користувач {update.effective_user.username} натиснув кнопку")

# Головна функція
def main():
    try:
        print("Запуск програми...")  # Додаткове логування
        token = os.getenv("BOT_TOKEN")  # Токен отримується зі змінної середовища
        if not token:
            raise ValueError("BOT_TOKEN не знайдено у змінних середовища.")

        # URL для Webhook
        port = int(os.getenv("PORT", 8443))  # Отримуємо порт від Render або 8443 за замовчуванням
        webhook_url = os.getenv("RENDER_EXTERNAL_URL", "https://localhost") + "/webhook"

        print(f"Порт: {port}")
        print(f"Webhook URL: {webhook_url}")

        # Створення бота
        application = ApplicationBuilder().token(token).build()

        # Додавання обробників
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))

        # Налаштування Webhook
        print("Запуск Webhook...")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=webhook_url,
        )
    except Exception as e:
        print(f"Помилка під час запуску програми: {e}")

if __name__ == "__main__":
    main()
