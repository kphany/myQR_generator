from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm, UserLoginForm, QRCodeForm
from .models import QRCode
import io
import qrcode
from django.core.files.base import ContentFile
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import QRCodeSerializer
from rest_framework import generics
from django.http import JsonResponse, HttpResponseBadRequest
from .models import QRCode

def home(request):
    return render(request, 'qr_app/home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to home page after registration
    else:
        form = UserCreationForm()
    return render(request, 'qr_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'qr_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def generate_qr(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            data = form.cleaned_data['data']
            size = form.cleaned_data['size']
            color = form.cleaned_data['color']
            
            size_map = {
                'small': 200,
                'medium': 400,
                'large': 600
            }
            qr_size = size_map.get(size, 400)
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=color, back_color='white')
            img = img.resize((qr_size, qr_size))
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_content = ContentFile(buffer.getvalue(), name='temp.png')
            
            filename_safe_data = re.sub(r'[^a-zA-Z0-9]', '_', data)
            filename = f'{filename_safe_data}.png'
            
            qr_code = QRCode(user=request.user, title=title, data=data, size=size, color=color)
            qr_code.image.save(filename, img_content)
            
            # Update the QR code data to include the scan URL
            scan_url = request.build_absolute_uri(reverse('scan_qr_code', args=[qr_code.pk]))
            qr_code.data = scan_url
            qr_code.save()

            return render(request, 'qr_app/qr_code.html', {'qr_code': qr_code})
    else:
        form = QRCodeForm()
    return render(request, 'qr_app/generate.html', {'form': form})

@login_required
def list_qr_codes(request):
    qr_codes = QRCode.objects.filter(user=request.user)
    return render(request, 'qr_app/list_qr_codes.html', {'qr_codes': qr_codes})

@login_required
def delete_qr_code(request, pk):
    qr_code = get_object_or_404(QRCode, pk=pk, user=request.user)
    
    if request.method == 'POST':
        qr_code.image.delete()  # Remove the image file from the server
        qr_code.delete()  # Delete the QR code record from the database
        return HttpResponseRedirect(reverse('list_qr_codes'))
    
    return render(request, 'qr_app/delete_qr_code.html', {'qr_code': qr_code})

@login_required
def edit_qr_code(request, pk):
    qr_code = get_object_or_404(QRCode, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = QRCodeForm(request.POST, instance=qr_code)
        if form.is_valid():
            form.save()
            return redirect('list_qr_codes')
    else:
        form = QRCodeForm(instance=qr_code)
    
    return render(request, 'qr_app/edit_qr_code.html', {'form': form, 'qr_code': qr_code})

@login_required
def download_qr_code(request, pk):
    qr_code = get_object_or_404(QRCode, pk=pk, user=request.user)
    with open(qr_code.image.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/png")
        response['Content-Disposition'] = f'attachment; filename="{qr_code.title}.png"'
        return response

def scan_qr_code(request, pk):
    qr_code = get_object_or_404(QRCode, pk=pk)
    
    # Increment the scan count
    qr_code.scans += 1
    qr_code.save()

    # Serve the QR code image
    with open(qr_code.image.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/png")
        response['Content-Disposition'] = f'inline; filename="{qr_code.title}.png"'
        return response
    
def track_qr_code_scan(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, id=qr_code_id)
    qr_code.scans += 1
    qr_code.save()
    # Redirect or respond accordingly

def track_scan(request, qr_code_id):
    try:
        qr_code = QRCode.objects.get(id=qr_code_id)
        qr_code.scans += 1
        qr_code.save()
        return JsonResponse({'status': 'success', 'scans': qr_code.scans})
    except QRCode.DoesNotExist:
        return HttpResponseBadRequest('QR Code not found')

class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

class QRCodeListCreateView(generics.ListCreateAPIView):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

class QRCodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer