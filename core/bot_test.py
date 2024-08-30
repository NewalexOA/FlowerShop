import telebot

TOKEN = "6929480003:AAGOqoWzHJd77T2Fk55coU7ZJ6FNh0JOGYU"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Здравствуйте! Этот бот будет уведомлять вас о новых заказах.')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы написали: {message.text}")

print("Бот запущен и ожидает сообщения...")
bot.polling()
