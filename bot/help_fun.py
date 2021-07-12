from telebot import types

from datetime import datetime
from pyzbar import pyzbar
import os


def mar():
	markup = types.InlineKeyboardMarkup()
	markup.row_width = 2
	markup.add(types.InlineKeyboardButton("Четные", callback_data="even"),
			   types.InlineKeyboardButton("Нечетные", callback_data="not_even"))
	return markup


def create_folder_and_save_img(fileID, chat_id, bot):
	file_info = bot.get_file(fileID)
	downloaded_file = bot.download_file(file_info.file_path)
	dir = f"{chat_id}{datetime.now()}{file_info.file_unique_id}"
	os.mkdir(dir)
	absolut_path = f"{os.getcwd()}/{dir}/{file_info.file_unique_id}.jpg"
	with open(absolut_path, 'wb') as new_file:
		new_file.write(downloaded_file)
	return absolut_path


def get_numbers(code):
	even = [i for i in code[0] if int(i) % 2 == 0]
	not_even = [i for i in code[0] if int(i) % 2 != 0]
	return even[0], not_even[-1]


def decode(image):
	decoded_objects = pyzbar.decode(image)
	if not decoded_objects:
		return False
	return decoded_objects[0]
