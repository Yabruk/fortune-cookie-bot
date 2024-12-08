import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from random import choice

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привіт! Натисни /fortune, щоб отримати своє передбачення!')

async def fortune(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(choice(FORTUNES))

def main() -> None:
    # Створюємо додаток з токеном
    application = Application.builder().token(TOKEN).build()

    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fortune", fortune))

    # Запускаємо polling
    application.run_polling()

if __name__ == '__main__':
    main()
