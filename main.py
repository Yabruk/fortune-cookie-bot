import os
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
    print(f"Користувач {update.effective_user.username} натиснув кнопку")
    query = update.callback_query
    await query.answer()  # Закриває "годинник" на кнопці
    if query.data == "get_fortune":
        fortune = random.choice(FORTUNES)
        await query.edit_message_text(f"✨ Твоє передбачення: {fortune}")

# Головна функція
def main():
    token = os.getenv("BOT_TOKEN")  # Токен отримується з середовища
    if not token:
        raise ValueError("BOT_TOKEN не знайдено у змінних середовища.")

    # URL для Webhook
    webhook_url = os.getenv("RENDER_EXTERNAL_URL") + "/webhook"

    # Створення бота
    application = ApplicationBuilder().token(token).build()

    # Додавання обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Налаштування Webhook
    application.run_webhook(
        
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        webhook_url=webhook_url,
    )
    # Після виклику application.run_webhook
    print(f"Webhook встановлено: {webhook_url}")

if __name__ == "__main__":
    main()
