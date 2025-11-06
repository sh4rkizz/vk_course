from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.conf.urls.static import static

from questions.views import index_view

urlpatterns = [
    re_path(r'^gramm/', include('gramm.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^questions/', include('questions.urls')),
    # re_path(r'', index_view, name='index_view'),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns = [re_path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
