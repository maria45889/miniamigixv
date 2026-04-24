from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 🔧 Admin
    path('admin/', admin.site.urls),

    # 🔑 Google OAuth (allauth)
    path('accounts/', include('allauth.urls')),

    # 💬 App principal
    path('', include('chat.urls')),
]

# 🖼️ Servir archivos MEDIA en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    