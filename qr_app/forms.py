from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import QRCode

class QRCodeForm(forms.ModelForm):
    class Meta:
        model = QRCode
        fields = ['title', 'data', 'size', 'color']
        widgets = {
            'data': forms.Textarea(attrs={'rows': 4}),
            'size': forms.Select(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')]),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    pass
