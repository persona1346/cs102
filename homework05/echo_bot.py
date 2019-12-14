import telebot


access_token = '900766027:AAG959h1iKxWgD7UZV-jbC6a8xnWMIK7st4'
telebot.apihelper.proxy = {'https': 'socks5h://94.138.147.2:3129'}

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)


# Бот будет отвечать только на текстовые сообщения
@bot.message_handler(content_types=['text'])
def echo(message: str) -> None:
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling()
