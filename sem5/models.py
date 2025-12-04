from django.db import IntegrityError, models


class LikeManager(models.Manager):
    def like_image(self, image, user):
        try:
            like = self.create(image=image, user=user)
            return like, True
        except IntegrityError as db_exception:
            like = self.filter(image=image, user=user).first()
            print(f"Failed when leaving like: {db_exception}")
            return like, False


class Image(models.Model):
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to="uploads/")
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    likes_cnt = models.IntegerField(default=0, help_text="[Денормализация]")


class ImageLike(models.Model):
    class Meta:
        unique_together = ("image", "user")

    image = models.ForeignKey("sem5.Image", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
