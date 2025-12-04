from django.urls import re_path

from sem51.views import LikeImageView, index_view


app_name = "sem51"
urlpatterns = [
    re_path(r'^(?P<id>\d+)/like', LikeImageView.as_view(), name="like"),
    re_path(r'^', index_view, name="image_view"),
]