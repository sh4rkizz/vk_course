from django.db import IntegrityError, models
from django.contrib.auth.models import User

class LikeManager(models.Manager):
    def leave_like(self, image, user, vote_type):
        query = {"image": image, "user": user}

        user_like = self.filter(**query).first()
        if user_like is not None:
            if user_like.vote_type != vote_type:
                user_like.vote_type = vote_type
                user_like.save(update_fields=["vote_type"])
                return user_like
            else:
                user_like.is_active = not user_like.is_active
                return user_like

        try:
            user_like = UserImageLike.objects.create(**query)
        except IntegrityError as db_error:
            print(db_error)
            user_like = self.filter(**query).first()
            user_like.is_active = not user_like.is_active
            user_like.save(update_fields=["is_active"])
        return user_like


def get_upload_userimage_path(instance):
    ...

class UserImage(models.Model):
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to=get_upload_userimage_path)

    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    likes_cnt = models.IntegerField(default=0, help_text="[Денормализация]")


class UserImageLike(models.Model):
    TYPE_CHOICES = (
        ("like", "Лайк"),
        ("dislike", "дизайк"),
    )
    class Meta:
        unique_together = ["user", "image"]

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="likes")
    image = models.ForeignKey("sem51.UserImage", on_delete=models.CASCADE, related_name="likes")
    vote_type = models.CharField(choices=TYPE_CHOICES, max_length=16)

    is_active = models.BooleanField(default=True)

    objects = LikeManager()
