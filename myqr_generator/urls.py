from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line if using built-in auth views
    path('', include('qr_app.urls')),  # Include qr_app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
