from telegram.ext import Updater, CommandHandler
import random
from flask import Flask
from threading import Thread

# Список передбачень
predictions = [
    "Сьогодні твій день!",
    "На тебе чекає несподівана зустріч.",
    "Усмішка відкриє нові двері.",
    "Тримайся, все буде добре!",
    "Завтра буде краще, ніж сьогодні."
]

# Функція для команди /start
def start(update, context):
    update.message.reply_text("Привіт! Натисни /predict, щоб отримати своє передбачення!")

# Функція для команди /predict
def predict(update, context):
    prediction = random.choice(predictions)
    update.message.reply_text(f"Твоє передбачення: {prediction}")

# Налаштування бота
TOKEN = ""  # Вставте свій токен
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("predict", predict))

# Створення вебсерверу для UptimeRobot
app = Flask('')

@app.route('/')
def home():
    return "Бот працює!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Запуск бота та вебсерверу
Thread(target=run).start()
updater.start_polling()
updater.idle()
