# qr_app/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class QRCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    image = models.ImageField(upload_to='qr_codes/')
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=7, default='#000000')  # Add this line if needed
    scans = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class QRCodeHistory(models.Model):
    qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return f"{self.qrcode.title} - {self.action}"
