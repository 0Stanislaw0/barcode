from django.contrib import admin
from .models import BarCode, UserPhoto, User


class UserPhotoAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'photo_id')
	ordering = ('-photo_id', 'user_id',)
	search_fields = ['user_id_id', ]


admin.site.register(BarCode)
admin.site.register(User)
admin.site.register(UserPhoto, UserPhotoAdmin)
