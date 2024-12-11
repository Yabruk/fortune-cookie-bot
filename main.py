import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

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
def fortune_cookie(update: Update, context: CallbackContext) -> None:
    fortune = random.choice(fortunes)
    update.message.reply_text(f"Ваше передбачення: {fortune}")

def main():
    # Замініть на ваш токен
    token = 'YOUR_BOT_TOKEN'

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Обробник команд
    dispatcher.add_handler(CommandHandler("fortune", fortune_cookie))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
