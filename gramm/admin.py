from django.contrib import admin

from gramm.models import Comment, CommentLikes, Post, PostLikes, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ['author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...


@admin.register(PostLikes)
class PostLikesAdmin(admin.ModelAdmin):
    ...


@admin.register(CommentLikes)
class CommentLikesAdmin(admin.ModelAdmin):
    ...
