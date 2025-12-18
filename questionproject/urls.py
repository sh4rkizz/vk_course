from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^questions/', include('questions.urls')),
    re_path(r'^sem7/', include('sem7.urls', namespace="sem7"))
]
