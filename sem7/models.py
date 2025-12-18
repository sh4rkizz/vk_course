from django.db import models


class Message(models.Model):
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    chat = models.ForeignKey("sem7.Chat", verbose_name="Чат", on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey("auth.User", verbose_name="Автор сообщения", on_delete=models.CASCADE)

    text = models.TextField(verbose_name="Текст сообщения", max_length=4000)
    created_at = models.DateTimeField(verbose_name="Создано в", auto_now_add=True)

    def __str__(self):
        return f"Сообщение #{self.pk} в чате #{self.chat_id} от пользователя #{self.author_id}"


class Chat(models.Model):
    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self):
        return f"Чат #{self.pk}"


class UserInChat(models.Model):
    class Meta:
        verbose_name = "Пользователь в чате"
        verbose_name_plural = "Пользователи в чатах"
        unique_together = ["chat", "user"]

    chat = models.ForeignKey("sem7.Chat", verbose_name="Чат", on_delete=models.CASCADE, related_name="users_in_chats")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="users_in_chats")

    def __str__(self):
        return f"Пользователь #{self.user_id} в чате #{self.chat_id}"
