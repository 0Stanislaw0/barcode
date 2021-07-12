import redis
from decouple import config

r = redis.Redis(host=config('REDIS_HOST', cast=str))

import config


def get_current_state(user_id):
	try:
		return int(r.get(user_id))
	except KeyError:
		return config.States.S_START.value


def set_state(user_id, value):
	r.set(user_id, value)
