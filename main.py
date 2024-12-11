import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Список передбачень для "печива"
fortunes = [
    "Твоя удача сьогодні в руках!",
    "Завтра принесе нові можливості.",
    "Не бійтеся змін – вони на краще.",
    "Нехай ваш шлях буде легким і ясним.",
    "Ваші мрії скоро збудуться!",
    "Сьогодні - день великих досягнень!",
    "Ваша мудрість допоможе знайти правильний шлях.",
    "Не зупиняйтесь, якщо сьогодні не все йде за планом."
]

# Функція для видачі передбачення
async def fortune_cookie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    fortune = random.choice(fortunes)
    await update.message.reply_text(f"Ваше передбачення: {fortune}")

def main():
    # Отримуємо токен з змінної середовища
    token = os.getenv('BOT_TOKEN')

    if not token:
        print("Токен не знайдено! Перевірте змінну середовища BOT_TOKEN.")
        return

    # Створення додатку
    application = Application.builder().token(token).build()

    # Обробник команд
    application.add_handler(CommandHandler("fortune", fortune_cookie))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
