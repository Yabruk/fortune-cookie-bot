import os
import asyncio
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

# ID анімованого стікера печива (замініть на свій стікер)
COOKIE_STICKER_ID = "CAACAgEAAxkBAAEK8H9nXwj-Y9LWlnWE37D_jkmOTED_QgAC_QIAAo11IEQSMwdGJ3a-hjYE"

# Flask додаток для запуску на Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

# Асинхронна функція для команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Створюємо меню з однією кнопкою
    keyboard = [
        [InlineKeyboardButton("Печенька", callback_data="get_fortune")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Відправляємо повідомлення стану
    status_message = await update.message.reply_text("У мене для тебе щось є..")
    
    # Відправляємо меню
    menu_message = await update.message.reply_text("Ось, тримай печеньку", reply_markup=reply_markup)

    # Видаляємо повідомлення користувача /start
    try:
        await update.message.delete()
    except Exception as e:
        print(f"Не вдалося видалити повідомлення користувача: {e}")

    # Зберігаємо ID статусного повідомлення у контексті
    context.chat_data['status_message'] = status_message

# Функція для обробки кнопки "Печенька"
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Підтверджуємо отримання callback'у

    # Видаляємо початкове повідомлення з кнопкою
    try:
        await query.message.delete()
    except Exception as e:
        print(f"Не вдалося видалити повідомлення: {e}")

    # Створюємо асинхронну задачу для обробки подій після натискання кнопки
    asyncio.create_task(handle_cookie_animation(query, context))

# Асинхронна функція для обробки анімації, передбачення і таймера
async def handle_cookie_animation(query, context):
    # Отримуємо статусне повідомлення
    status_message = context.chat_data.get('status_message')

    # Оновлюємо статус: "Секундочку..."
    if status_message:
        try:
            await status_message.edit_text("Секундочку...")
        except Exception as e:
            print(f"Не вдалося оновити статус: {e}")

    # Відправляємо анімований стікер
    sticker_message = await query.message.chat.send_sticker(COOKIE_STICKER_ID)
    await asyncio.sleep(2)  # Чекаємо, поки анімація програється

    # Видаляємо стікер
    try:
        await sticker_message.delete()
    except Exception as e:
        print(f"Не вдалося видалити стікер: {e}")

    # Оновлюємо статус: "Твоє передбачення на сьогодні"
    if status_message:
        try:
            await status_message.edit_text("Твоє передбачення на сьогодні")
        except Exception as e:
            print(f"Не вдалося оновити статус: {e}")

    # Відправляємо передбачення з моношрифтом
    fortune_message = await query.message.chat.send_message(f"`{choice(FORTUNES)}`", parse_mode="MarkdownV2")

    # Чекаємо 2 хвилини, потім видаляємо передбачення
    await asyncio.sleep(120)
    try:
        await fortune_message.delete()
    except Exception as e:
        print(f"Не вдалося видалити повідомлення з передбаченням: {e}")

    # Оновлюємо статус: "У мене для тебе щось є.."
    if status_message:
        try:
            await status_message.edit_text("У мене для тебе щось є..")
        except Exception as e:
            print(f"Не вдалося оновити статус: {e}")

    # Показуємо меню з кнопкою
    keyboard = [
        [InlineKeyboardButton("Печенька", callback_data="get_fortune")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.chat.send_message("Ось, тримай печеньку", reply_markup=reply_markup)

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
