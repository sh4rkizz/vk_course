from django.db import models
from django.contrib.auth.models import User


class DefaultManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class PostManager(DefaultManager):
    def visible_for(self, user: User):
        from gramm.models import Post
        queryset = self
        is_authored_draft_filter = models.Q(status=Post.STATUS_DRAFT) & models.Q(author=user)

        if user.is_staff:
            visible_for_admin = models.Q(status__in=[Post.STATUS_PUBLISHED, Post.STATUS_ARCHIVED])
            queryset = queryset.filter(visible_for_admin | is_authored_draft_filter)
            return queryset

        is_published_filter = models.Q(status=Post.STATUS_PUBLISHED)
        return queryset.filter(is_published_filter | is_authored_draft_filter)
