import telebot
from telebot import types
import sqlite3
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def spysok(message_id):
	all_users = get_users()
	i = 1
	bot.send_message(message_id, "Список смердів: ")
	for person in all_users:
		if person in arr:
			pass
		else:
			bot.send_message(message_id,f"{i}.{person}")
			i += 1
	status_arr.clear()
	arr.clear()
	if len(arr) == len(all_users):
		pass
	else:
		bot.send_photo(message_id, open('von-.jpg', 'rb'))

sched = BlockingScheduler()
bot = telebot.TeleBot("5472931040:AAHPfwgbzn2OyISPpRLrsUwDhcxzBm-xDWU")
pereklychka = False
arr = []
status_arr = []


def get_users():
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	all_users = c.execute("SELECT id FROM users").fetchall()
	all_users = list(map(lambda x: str(x[0]), all_users))
	conn.commit()
	return all_users




@bot.message_handler(commands=['registration'])
def buda_going(message):
	username = message.from_user.username
	all_users = get_users()

	if username not in all_users:
		bot.send_message(message.chat.id, f"{message.from_user.first_name}, ви успішно зареєстровані на перекличку")
		conn = sqlite3.connect("users.db")
		c = conn.cursor()
		c.execute("INSERT INTO users VALUES(?,?)", (username,0))

		conn.commit()
	else:
		bot.reply_to(message, "Ти вже зареєстрований(-на), курва нахєра два рази реєструватись")


@bot.message_handler(commands=['pereklychka'])
def smerd_checker(message):
	if len(status_arr) == 0:
		status_arr.append(1)
		all_users = get_users()
		for user in all_users:
			bot.send_message(message.chat.id, "@"+user)

		markup1 = types.InlineKeyboardMarkup(row_width=1)
		item1 = types.InlineKeyboardButton('Я не смерд', callback_data='ne_smerd')
		markup1.add(item1)
		msg = bot.send_message(message.chat.id, 'Смердите?', reply_markup=markup1)
		start = datetime.datetime.now()
		end_time = start + datetime.timedelta(minutes=1)

		sched.add_job(lambda : bot.send_message(message.chat.id, "Перекличку завершено"), trigger="cron", hour=end_time.hour, minute=end_time.minute, second=end_time.second)
		sched.add_job(lambda : bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Голосування закрито', reply_markup=None)
					  , trigger="cron", hour=end_time.hour, minute=end_time.minute, second=end_time.second)
		sched.add_job(lambda: spysok(message.chat.id), trigger="cron", hour=end_time.hour, minute=end_time.minute, second=end_time.second+1)
		sched.start()
	else:
		bot.send_message(message.chat.id, "Перекличка вже триває")




@bot.message_handler(content_types=['text'])
def echo_all(message):
	if message.text == 'буда':
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton("Запрошення до буди", url="https://t.me/+Omv5EzIJ8o9jZjky"))
		bot.send_message(message.chat.id, 'Буда', reply_markup=markup)
	elif  'НАЛИВАЙ' in message.text.upper():
		markup_zabava = types.InlineKeyboardMarkup(row_width=1)
		stakan1 = types.InlineKeyboardButton('Потягнути', callback_data='potagnyv')
		markup_zabava.add(stakan1)

		bot.send_photo(message.chat.id, open('image001-296.jpg', 'rb'), reply_markup=markup_zabava)




@bot.callback_query_handler(func=lambda call: True)
def callback_status(call):
	if call.message:
		if call.data == 'ne_smerd':
			if call.from_user.username not in arr:
				arr.append(call.from_user.username)
				bot.answer_callback_query(callback_query_id=call.id, text='Молодець', show_alert=True)
		elif call.data == 'potagnyv':
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			bot.send_message(call.message.chat.id, f"{call.from_user.first_name} потягнув")


bot.infinity_polling()