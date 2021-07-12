from django.db import models


class BarCode(models.Model):
	file_id = models.CharField(max_length=100)
	data_code = models.CharField(max_length=50)
	path_to_file = models.CharField(max_length=255)

	def __str__(self):
		return "Данные штрих кода: {} ".format(str(self.data_code))


class User(models.Model):
	chat_id = models.IntegerField(unique=True)
	name = models.CharField(max_length=128)
	phone_number = models.CharField(max_length=12, null=True, blank=True)

	def __str__(self):
		return "chat id: {} ".format(str(self.chat_id))


class UserPhoto(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	photo_id = models.ForeignKey(BarCode, on_delete=models.CASCADE)
