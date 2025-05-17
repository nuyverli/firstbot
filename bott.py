import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Токен вашего бота (замените на свой)
TOKEN = "7772699831:AAEXXdVR6L3m-Z3n3gL4AeRXkxrQjOWhnOo"

async def get_usd_rate():
    """Получает текущий курс USD/RUB от Центробанка России"""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    data = response.json()
    usd_rate = data['Valute']['USD']['Value']
    return usd_rate

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "Привет! Я бот для проверки курса доллара.\n"
        "Нажми /usd чтобы узнать текущий курс USD/RUB."
    )

async def usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /usd"""
    try:
        rate = await get_usd_rate()
        await update.message.reply_text(f"Текущий курс USD/RUB: {rate:.2f} ₽")
    except Exception as e:
        await update.message.reply_text("Не удалось получить курс. Попробуйте позже.")

def main():
    """Запуск бота"""
    # Создаем Application вместо Updater
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("usd", usd))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()