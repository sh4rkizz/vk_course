from django.contrib import admin

from sem51.models import UserImage, UserImageLike

class UserImageAdmin(admin.ModelAdmin):
    pass

class UserImageLikeAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserImage, UserImageAdmin)
admin.site.register(UserImageLike, UserImageLikeAdmin)