from django.http import HttpResponse
from rest_framework import generics
from .models import SharedFile
from .serializers import SharedFileSerializer
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
from django.conf import settings
from .encryption import encrypt_file_content, decrypt_file_content, get_aes_key
class FileUploadView(generics.CreateAPIView):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer

class FileListView(generics.ListAPIView):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer



def home(request):
    return HttpResponse("Welcome to the Home Page")


def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    aes_key = get_aes_key()
    decrypted_content = decrypt_file_content(uploaded_file.encrypted_content, aes_key)
    response = HttpResponse(decrypted_content, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file_name}"'
    return response



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read()
            print("File content read successfully")
            aes_key = get_aes_key()
            print("AES key retrieved successfully")
            encrypted_content = encrypt_file_content(file_content, aes_key)
            print("File content encrypted successfully")
            UploadedFile.objects.create(
                file_name=uploaded_file.name,
                encrypted_content=encrypted_content
            )
            print("File saved to database successfully")
            return redirect('file_upload_success')
    else:
        form = UploadFileForm()
    return render(request, 'files/upload.html', {'form': form})


def file_upload_success(request):
    return HttpResponse("File uploaded successfully!")