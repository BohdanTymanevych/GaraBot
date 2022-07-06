import telebot
from telebot import types
import sqlite3
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler




sched = BlockingScheduler()
bot = telebot.TeleBot("5472931040:AAHPfwgbzn2OyISPpRLrsUwDhcxzBm-xDWU")
pereklychka = False

def get_users():
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	all_users = c.execute("SELECT id FROM users").fetchall()
	all_users = list(map(lambda x: str(x[0]), all_users))
	conn.commit()
	return all_users




@bot.message_handler(commands=['registration'])
def buda_going(message):
	bot.send_message(message.chat.id, 'Миронцю - професіонал своєї справи.')
	username = message.from_user.username
	all_users = get_users()

	if username not in all_users:
		conn = sqlite3.connect("users.db")
		c = conn.cursor()
		c.execute("INSERT INTO users VALUES(?,?)", (username,0))

		conn.commit()



@bot.message_handler(commands=['pereklychka'])
def smerd_checker(message):
	all_users = get_users()
	for user in all_users:
		bot.send_message(message.chat.id, "@"+user)

	markup1 = types.InlineKeyboardMarkup(row_width=2)
	item1 = types.InlineKeyboardButton('Я не смерд', callback_data='ne_smerd')
	item2 = types.InlineKeyboardButton('Підсмерджую', cacallback_data='smerd')
	markup1.add(item1,item2)
	msg = bot.send_message(message.chat.id, 'Смердите?', reply_markup=markup1)
	start = datetime.datetime.now()
	end_time = start + datetime.timedelta(minutes=3)


	sched.add_job(lambda : bot.send_message(message.chat.id, "Перекличку завершено"), trigger="cron", hour=end_time.hour, minute=end_time.minute)
	sched.add_job(lambda : bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Голосування закрито',reply_markup=None)
				  , trigger="cron", hour=end_time.hour, minute=end_time.minute)
	sched.start()







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

@bot.callback_query_handler(func=lambda call: True)
def callback_status(call):
	if call.message:
		if call.data == 'ne_smerd':
			print(call.message.from_user.username)




bot.infinity_polling()