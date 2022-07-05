import telebot
from telebot import types
import sqlite3
import datetime


bot = telebot.TeleBot("5472931040:AAHPfwgbzn2OyISPpRLrsUwDhcxzBm-xDWU")
pereklychka = False

def get_users():
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	all_users = c.execute("SELECT id FROM users").fetchall()
	all_users = list(map(lambda x: str(x[0]), all_users))
	conn.commit()
	return all_users




@bot.message_handler(commands=['start'])
def buda_going(message):
	bot.send_message(message.chat.id, 'Миронцю - професіонал своєї справи.')
	username = message.from_user.username
	all_users = get_users()

	if username not in all_users:
		conn = sqlite3.connect("users.db")
		c = conn.cursor()
		c.execute("INSERT INTO users VALUES(?,?)", (username,0))

		conn.commit()



@bot.message_handler(commands=['Перекличка'])
def smerd_checker(message):
	all_users = get_users()
	for user in all_users:
		bot.send_message(message.chat.id, "@"+user)


	markup1 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
	markup1.add(types.KeyboardButton("Я не смерд"))
	bot.send_message(message.chat.id, 'Смердите?', reply_markup=markup1)
	start = datetime.datetime.now()
	end_time = start + datetime.timedelta(minutes=10)







@bot.message_handler(content_types=['text'])
def echo_all(message):
	if message.text == 'наливай':
		photo = open('e9f3d3u-960.png', 'rb')
		bot.send_photo(message.chat.id, photo)
	elif message.text == 'буда':
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton("Запрошення до буди", url="https://t.me/+Omv5EzIJ8o9jZjky"))
		bot.send_message(message.chat.id, 'Буда', reply_markup=markup)
	else:
		bot.reply_to(message, message.text)





bot.infinity_polling()