import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = 'Чтобы начать работы введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>\n\
Увидеть список все доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')

        if len(val) > 3:
            raise ConvertionException('Всего должно быть 3 параметра, например доллар евро 3.')

        quote, base, amount = val
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base } - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
