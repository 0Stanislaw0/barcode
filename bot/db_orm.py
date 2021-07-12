import psycopg2
from config import params_db


def conn(func):
	""" Декоратор для транзакции операции """

	def decor(*args, **kwargs):
		with psycopg2.connect(**params_db) as conn:
			return func(*args, **kwargs, conn=conn)

	return decor


@conn
def write_chat_id_and_username(chat_id, username, conn=conn):
	"""Записывает ник и chat id пользователя"""
	conn.cursor().execute(
		"INSERT INTO users_user(chat_id, name) VALUES ('%s','%s') ON CONFLICT (chat_id) "
		"DO UPDATE SET name= '%s' " % (chat_id, username, username))
	conn.commit()


@conn
def write_phone_number(phone_number, chat_id, conn=conn):
	"""Записывает мобильный номер пользователя"""
	conn.cursor().execute(
		"UPDATE users_user SET phone_number = '%s' WHERE chat_id = '%s'" % (phone_number, chat_id))
	conn.commit()


@conn
def write_info_barcode(file_id, data, path_to_file, conn=conn):
	"""Записывает информацию о штрих-коде """
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO users_barcode(file_id,data_code,path_to_file) VALUES ('%s','%s','%s') RETURNING id" % (
			file_id, data, path_to_file))
	conn.commit()
	return cur.fetchone()[0]


@conn
def create_user_to_photo(photo, chat_id, conn=conn):
	"""Создает отношение Юзер-Фото  """
	cur = conn.cursor()
	cur.execute("SELECT id FROM users_user WHERE chat_id= '%s'" % (chat_id))
	user_id = cur.fetchone()[0]
	cur.execute(
		"INSERT INTO users_userphoto(user_id_id,photo_id_id) VALUES ('%s','%s') RETURNING id" % (user_id, photo))
	conn.commit()


@conn
def get_data_code(chat_id, conn=conn):
	""" Получает данные штрихкода последней удачно распознаной фотографии от пользователя"""
	cur = conn.cursor()
	cur.execute(
		"SELECT data_code FROM users_barcode WHERE id = (select max(photo_id_id) from users_user  left join users_userphoto on users_user.id=users_userphoto.user_id_id where chat_id = '%s') " % (
			chat_id))
	conn.commit()
	return list(cur.fetchall()[-1])
