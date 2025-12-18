from django.contrib import admin

from sem7.models import Chat, Message, UserInChat

admin.site.register(UserInChat)
admin.site.register(Message)
admin.site.register(Chat)
