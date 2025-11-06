# from gramm.views import IndexPostView
from django.urls import re_path

from gramm.views import index_post_view

app_name = "gramm"

urlpatterns = [
    re_path(r'^', index_post_view, name="index_posts_view"),
]
