from enum import Enum
from decouple import config

API_TOKEN = config('API_TOKEN', cast=str)

regex_pattern_number = '^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$'

params_db = {"host": config('DB_HOST', cast=str),
			 "database": config('DB_NAME', cast=str),
			 "user": config('DB_USER', cast=str),
			 "password": config('DB_PASSWORD', cast=str)}


class States(Enum):
	S_START = 0  # Начало нового диалога
	S_ENTER_NAME = 1
	S_ENTER_NUMBER = 2
	S_ENTER_PIC = 3
	S_SEND_DIGIT = 4
