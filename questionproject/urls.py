from django.urls import include, re_path
from django.contrib import admin
from django.conf.urls.static import static

from questionproject import settings

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^questions/', include('questions.urls')),
    re_path(r'^sem5/', include('sem5.urls', namespace="sem5"))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
