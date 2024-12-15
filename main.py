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

# ID анімованого стікера печива
COOKIE_STICKER_ID = "CAACAgEAAxkBAAEK8H9nXwj-Y9LWlnWE37D_jkmOTED_QgAC_QIAAo11IEQSMwdGJ3a-hjYE"

# Шляхи до файлів передбачень
MORNING_FORTUNES_FILE = "morning_fortunes.json"
DAILY_FORTUNES_FILE = "daily_fortunes.json"
EVENING_FORTUNES_FILE = "evening_fortunes.json"

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def get_fortunes_file():
    now = datetime.now().time()
    if now >= datetime.strptime("04:00", "%H:%M").time() and now < datetime.strptime("12:00", "%H:%M").time():
        return MORNING_FORTUNES_FILE
    elif now >= datetime.strptime("12:00", "%H:%M").time() and now < datetime.strptime("17:00", "%H:%M").time():
        return DAILY_FORTUNES_FILE
    else:
        return EVENING_FORTUNES_FILE

def load_fortunes():
    fortunes_file = get_fortunes_file()
    if not os.path.exists(fortunes_file):
        raise FileNotFoundError(f"Файл {fortunes_file} не знайдено")
    with open(fortunes_file, "r", encoding="utf-8") as f:
        return json.load(f), fortunes_file

def save_fortunes(fortunes, fortunes_file):
    with open(fortunes_file, "w", encoding="utf-8") as f:
        json.dump(fortunes, f, ensure_ascii=False, indent=4)

def get_random_fortune():
    fortunes, fortunes_file = load_fortunes()
    now = datetime.now()

    available_fortunes = [
        fortune for fortune in fortunes
        if not fortune["last_used"] or 
        (datetime.strptime(fortune["last_used"], "%Y-%m-%d") < now - timedelta(days=30))
    ]

    if not available_fortunes:
        return None

    selected_fortune = choice(available_fortunes)

    for fortune in fortunes:
        if fortune["text"] == selected_fortune["text"]:
            fortune["last_used"] = now.strftime("%Y-%m-%d")
            break

    save_fortunes(fortunes, fortunes_file)
    return selected_fortune["text"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Печенько", callback_data="get_fortune")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    status_message = await update.message.reply_text("У мене для тебе щось є..")
    menu_message = await update.message.reply_text("Ось, тримай печеньку", reply_markup=reply_markup)

    try:
        await update.message.delete()
    except Exception:
        pass

    context.chat_data['status_message'] = status_message

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    try:
        await query.message.delete()
    except Exception:
        pass

    asyncio.create_task(handle_cookie_animation(query, context))

async def handle_cookie_animation(query, context):
    status_message = context.chat_data.get('status_message')

    if status_message:
        try:
            await status_message.edit_text("Секундочку...")
        except Exception:
            pass

    sticker_message = await query.message.chat.send_sticker(COOKIE_STICKER_ID)
    await asyncio.sleep(2)

    try:
        await sticker_message.delete()
    except Exception:
        pass

    if status_message:
        try:
            await status_message.edit_text("Твоє передбачення на сьогодні")
        except Exception:
            pass

    fortune = get_random_fortune()
    if fortune is None:
        fortune = "Усі передбачення використано. Поверніться пізніше!"

    fortune_message = await query.message.chat.send_message(
        f"<code>{fortune}</code>", parse_mode="HTML"
    )
    await asyncio.sleep(28800)

    try:
        await fortune_message.delete()
    except Exception:
        pass

    if status_message:
        try:
            await status_message.edit_text("У мене для тебе щось є..")
        except Exception:
            pass

    keyboard = [[InlineKeyboardButton("Печенько", callback_data="get_fortune")]]
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
