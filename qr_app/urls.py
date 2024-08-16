from django.urls import path
from . import views
from .views import QRCodeListCreateView, QRCodeRetrieveUpdateDestroyView

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.generate_qr, name='generate_qr'),
    path('list/', views.list_qr_codes, name='list_qr_codes'),
    path('delete/<int:pk>/', views.delete_qr_code, name='delete_qr_code'),
    path('generate/', views.generate_qr, name='generate_qr'),
    path('saved/', views.list_qr_codes, name='list_qr_codes'),
    path('qr_codes/<int:pk>/edit/', views.edit_qr_code, name='edit_qr_code'),
    path('qr_codes/<int:pk>/download/', views.download_qr_code, name='download_qr_code'),
    path('qr_codes/<int:pk>/scan/', views.scan_qr_code, name='scan_qr_code'),
    path('login/', views.login_view, name='login'),  # Custom login view
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('qrcodes/', QRCodeListCreateView.as_view(), name='api_qrcode_list_create'),
    path('qrcodes/<int:pk>/', QRCodeRetrieveUpdateDestroyView.as_view(), name='api_qrcode_detail'),
]



