import telebot
import redis_db
import re
from telebot import types
from config import States, regex_pattern_number, API_TOKEN
from help_fun import mar, create_folder_and_save_img, get_numbers, decode
from PIL import Image
from db_orm import write_chat_id_and_username, write_phone_number, write_info_barcode, create_user_to_photo, \
	get_data_code

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
	"""Начинает диалог сначала"""
	bot.send_message(message.chat.id, "Что ж, начнём по-новой. Как тебя зовут?")
	redis_db.set_state(message.chat.id, States.S_ENTER_NAME.value)


@bot.message_handler(commands=["step_back"])
def step_back(message):
	"""Делаем шаг назад. Дает возможность пользователю изменить вводимые данные"""
	bot.send_message(message.chat.id, "Вернемся немножко назад")
	current_state = redis_db.get_current_state(message.chat.id)
	state = 0 if current_state == 0 else current_state - 1
	redis_db.set_state(message.chat.id, state)


@bot.message_handler(commands=["start"])
def cmd_start(message):
	"""Начинаем диалог"""
	bot.send_message(message.chat.id, "Привет! Как я могу к тебе обращаться?")
	redis_db.set_state(message.chat.id, States.S_ENTER_NAME.value)


@bot.message_handler(
	func=lambda message: redis_db.get_current_state(message.chat.id) == States.S_ENTER_NAME.value)
def user_entering_name(message):
	"""Ожидаем имя от пользователя и просим его тел номер"""
	write_chat_id_and_username(message.chat.id, message.text)
	mark = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	key = types.KeyboardButton('Поделиться своим номером телефона', request_contact=True)
	mark.add(key)
	redis_db.set_state(message.chat.id, States.S_ENTER_NUMBER.value)
	bot.send_message(message.chat.id, "Теперь укажи, пожалуйста, свой телефонный номер или нажми на кнопку.",
					 reply_markup=mark)


@bot.message_handler(content_types=['contact'])
@bot.message_handler(
	func=lambda message: redis_db.get_current_state(message.chat.id) == States.S_ENTER_NUMBER.value)
def user_entering_phone_number(message):
	"""Ожидаем номер от пользователя и просим прислать фотографию со штрихкодом"""
	try:
		number = message.contact.phone_number
	except AttributeError as e:
		number = re.match(regex_pattern_number, message.text)
		if number:
			number = number[0]
		else:
			redis_db.set_state(message.chat.id, States.S_ENTER_NAME.value)

	if not number:
		user_entering_name(message)
	else:
		redis_db.set_state(message.chat.id, States.S_ENTER_PIC.value)
		write_phone_number(number, message.chat.id)
		bot.send_message(message.chat.id, f"Пришли фотографию со штрихкодом")


@bot.message_handler(content_types=['photo'])
@bot.message_handler(
	func=lambda message: redis_db.get_current_state(message.chat.id) == States.S_ENTER_PIC.value)
def user_send_photo(message):
	"""Ожидаем фото от пользователя, распознаем штрихкод, записываем в бд.
	 Отдаем клавиатуру с возможностью выбрать первое четное число и последнее нечетное из данных штрих кода"""
	chat_id = message.chat.id
	try:
		file_id = message.photo[-1].file_id
	except:
		bot.send_message(message.chat.id, "Ууупс. что-то не так. Не удалось распознать штрих код")
		return
	absolut_path = create_folder_and_save_img(message.photo[-1].file_id, chat_id, bot)
	image = decode(Image.open(absolut_path))
	if image:
		redis_db.set_state(chat_id, States.S_SEND_DIGIT.value)
		bot.send_message(chat_id, f"Найден ШК с  номером {int(image.data)}", reply_markup=mar())
		photo_id = write_info_barcode(message.photo[-1].file_id, int(image.data), absolut_path)
		create_user_to_photo(photo_id, chat_id)
	else:
		bot.send_message(message.chat.id, "Ууупс. что-то не так. Не удалось распознать штрих код")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	code = get_data_code(call.from_user.id)
	even, not_even = get_numbers(code)
	if call.data == "even":
		bot.answer_callback_query(call.id, f'{even}')
	elif call.data == "not_even":
		bot.answer_callback_query(call.id, f'{not_even}')


bot.polling()
