# qr_app/admin.py

from django.contrib import admin
from .models import QRCode, QRCodeHistory  # Ensure QRCodeHistory is imported

class QRCodeHistoryInline(admin.TabularInline):
    model = QRCodeHistory
    extra = 1

class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'data', 'size', 'image', 'scans', 'created_at')
    list_filter = ('created_at', 'scans')
    search_fields = ('title', 'data')

admin.site.register(QRCode, QRCodeAdmin)


