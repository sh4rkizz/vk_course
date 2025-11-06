from django.db import models
from django.contrib.auth.models import User

from gramm.managers import DefaultManager, PostManager
from django.db.models import Index

class UserProfile(models.Model):
    avatar = models.CharField(verbose_name="Аватарка пользователя", max_length=255)
    bio = models.TextField(verbose_name="Описание", max_length=4000)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)


class Post(models.Model):
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"
    STATUS_DRAFT = "draft"

    STATUS_CHOICES = (
        (STATUS_PUBLISHED, "Опубликован"),
        (STATUS_ARCHIVED, "Архивирован"),
        (STATUS_DRAFT, "Черновик"),
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    title = models.CharField(verbose_name="Название поста", max_length=255)
    content = models.TextField(verbose_name="Контент", max_length=4000)
    author = models.ForeignKey(User, verbose_name="Автор поста", on_delete=models.SET_NULL, null=True, related_name="user_posts")

    status = models.CharField(verbose_name="Статус опубликованности", choices=STATUS_CHOICES, default=STATUS_DRAFT)

    created_at = models.DateTimeField(verbose_name="Время создания поста", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="Время редактирования поста", auto_now=True)

    is_active = models.BooleanField(verbose_name="Активно?", help_text="Если TRUE - отображается пользователям", default=True)

    # comments_cnt = models.IntegerField(_(""))

    objects = PostManager()
    # active = ActiveManager()

    def __str__(self):
        return f"Пост #{self.id}: {self.title}"


class Comment(models.Model):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    content = models.TextField(verbose_name="Контент", max_length=4000)
    author = models.ForeignKey(User, verbose_name="Автор поста", on_delete=models.SET_NULL, null=True)
    parent_comment = models.ForeignKey("gramm.Comment", verbose_name="Корневой комментарий", null=True, blank=True, default=None, on_delete=models.CASCADE)
    post = models.ForeignKey("gramm.Post", verbose_name="Пост", on_delete=models.CASCADE, related_name="comments")

    created_at = models.DateTimeField(verbose_name="Время создания поста", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Время редактирования поста", auto_now=True)


class PostLikes(models.Model):
    class Meta:
        verbose_name = "Лайк к посту"
        verbose_name_plural = "Лайки к постам"
        unique_together = ['user', 'post']

    post = models.ForeignKey("gramm.Post", verbose_name="Пост", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)


class CommentLikes(models.Model):
    class Meta:
        verbose_name = "Лайк к коментарию"
        verbose_name_plural = "Лайки к коментариям"
        unique_together = ['user', 'comment']

    comment = models.ForeignKey("gramm.Comment", verbose_name="Комментарий", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)


class Question(models.Model):
    author = models.ForeignKey(User, verbose_name="Автор поста", on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField("gramm.QuestionTag")


class QuestionTag(models.Model):
    name = models.CharField(_(""), max_length=50)

