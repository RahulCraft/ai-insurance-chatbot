from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chatapp.views import chat_ui   

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('chatapp.urls')),

    # UI route (MAIN FIX )
    path('', chat_ui),
]

# Media files serve
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)