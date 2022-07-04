import telebot
from telebot import types

bot = telebot.TeleBot("5472931040:AAHPfwgbzn2OyISPpRLrsUwDhcxzBm-xDWU")

photo = open('e9f3d3u-960.png', 'rb')

@bot.message_handler(commands=['start', 'help','буда'])
def buda_going(message):
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("Запрошення до буди", url="https://t.me/+Omv5EzIJ8o9jZjky"))
	bot.send_message(message.chat.id, 'Буда', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	if message.text == 'наливай':
		photo = open('e9f3d3u-960.png', 'rb')
		bot.send_photo(message.chat.id, photo)
	else:
		bot.reply_to(message, message.text)



bot.infinity_polling()