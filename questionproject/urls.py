from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^questions/', include('questions.urls')),
    re_path(r'^sem51/', include('sem51.urls', namespace="sem51"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
