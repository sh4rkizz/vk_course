from django.urls import include, re_path
from django.contrib import admin

from questions.views import index_view

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^questions/', include('questions.urls')),
    re_path(r'', index_view, name='index_view'),
]
