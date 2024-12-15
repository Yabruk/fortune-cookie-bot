import os
import asyncio
import json
from datetime import datetime, timedelta
from random import choice
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask

# Отримуємо токен із змінного середовища
TOKEN = os.getenv('BOT_TOKEN')

# ID анімованого стікера печива (замініть на свій стікер)
COOKIE_STICKER_ID = "CAACAgEAAxkBAAEK8H9nXwj-Y9LWlnWE37D_jkmOTED_QgAC_QIAAo11IEQSMwdGJ3a-hjYE"

# Шлях до файлу передбачень
FORTUNES_FILE = "fortunes.json"

# Flask додаток для запуску на Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

# Завантаження передбачень із файлу
def load_fortunes():
    if not os.path.exists(FORTUNES_FILE):
        raise FileNotFoundError(f"Файл {FORTUNES_FILE} не знайдено")
    with open(FORTUNES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Збереження передбачень у файл
def save_fortunes(fortunes):
    with open(FORTUNES_FILE, "w", encoding="utf-8") as f:
        json.dump(fortunes, f, ensure_ascii=False, indent=4)

# Вибір випадкового передбачення
def get_random_fortune():
    fortunes = load_fortunes()
    now = datetime.now()

    # Фільтруємо передбачення за датою останнього використання
    available_fortunes = [
        fortune for fortune in fortunes
        if not fortune["last_used"] or 
        (datetime.strptime(fortune["last_used"], "%Y-%m-%d") < now - timedelta(days=30))
    ]

    if not available_fortunes:
        # Якщо немає доступних передбачень
        return None

    # Вибираємо випадкове передбачення
    selected_fortune = choice(available_fortunes)

    # Оновлюємо дату останнього використання
    for fortune in fortunes:
        if fortune["text"] == selected_fortune["text"]:
            fortune["last_used"] = now.strftime("%Y-%m-%d")
            break

    # Зберігаємо файл із оновленим передбаченням
    save_fortunes(fortunes)

    return selected_fortune["text"]

# Асинхронна функція для команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Печенька", callback_data="get_fortune")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    status_message = await update.message.reply_text("У мене для тебе щось є..")
    menu_message = await update.message.reply_text("Ось, тримай печеньку", reply_markup=reply_markup)

    try:
        await update.message.delete()
    except Exception as e:
        print(f"Не вдалося видалити повідомлення користувача: {e}")

    context.chat_data['status_message'] = status_message

# Функція для обробки кнопки "Печенька"
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    try:
        await query.message.delete()
    except Exception as e:
        print(f"Не вдалося видалити повідомлення: {e}")

    asyncio.create_task(handle_cookie_animation(query, context))

# Асинхронна функція для обробки анімації, передбачення і таймера
async def handle_cookie_animation(query, context):
    status_message = context.chat_data.get('status_message')

    # Оновлюємо статус: "Секундочку..."
    if status_message:
        try:
            await status_message.edit_text("Секундочку...")
        except Exception as e:
            print(f"Не вдалося оновити статус: {e}")

    # Відправляємо анімований стікер
    sticker_message = await query.message.chat.send_sticker(COOKIE_STICKER_ID)
    await asyncio.sleep(2)

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

    # Отримуємо передбачення через функцію
    fortune = get_random_fortune()
    if fortune is None:
        fortune = "Усі передбачення використано. Поверніться пізніше!"

    # Відправляємо передбачення з моношрифтом
    fortune_message = await query.message.chat.send_message(
        f"<code>{fortune}</code>", parse_mode="HTML"
    )
    await asyncio.sleep(120)

    # Видаляємо передбачення через 2 хвилини
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

    # Повертаємо меню з кнопкою
    keyboard = [[InlineKeyboardButton("Печенька", callback_data="get_fortune")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.chat.send_message("Ось, тримай печеньку", reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    from threading import Thread

    def run_flask():
        app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

    thread = Thread(target=run_flask)
    thread.start()
    main()
