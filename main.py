import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

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

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привіт! Натисни /fortune, щоб отримати своє передбачення!')

def fortune(update: Update, context: CallbackContext) -> None:
    from random import choice
    update.message.reply_text(choice(FORTUNES))

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("fortune", fortune))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
