from django.urls import re_path

from sem5.views import LikeImageView, index_view


app_name = "sem5"
urlpatterns = [
    re_path(r'^(?P<id>\d+)/like', LikeImageView.as_view(), name="like"),
    re_path(r'^', index_view, name="sem5_image_view"),
]
