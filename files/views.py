import base64
import mimetypes
from django.http import Http404, HttpResponse
from rest_framework import generics
from .models import SharedFile
from .serializers import SharedFileSerializer
from django.http import JsonResponse
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

def upload_file(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        encrypted_content = request.POST.get('encrypted_content')
        if file_name and encrypted_content:
            UploadedFile.objects.create(
                file_name=file_name,
                encrypted_content=encrypted_content
            )
            # print(encrypted_content, 'Encrypted Content')
            return JsonResponse({'message': 'File uploaded successfully'})
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def download_file(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        raise Http404("File does not exist")

    aes_key = get_aes_key()
    decrypted_content = decrypt_file_content(uploaded_file.encrypted_content, aes_key)
    encoded_content = base64.b64encode(decrypted_content).decode('utf-8')
    
    return JsonResponse({'file_name': uploaded_file.file_name, 'content': encoded_content})

def list_uploaded_files(request):
    files = UploadedFile.objects.all().values('id', 'file_name', 'uploaded_at')
    return JsonResponse(list(files), safe=False)

def delete_file(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        uploaded_file.delete()
        return JsonResponse({'message': 'File deleted successfully'})
    except UploadedFile.DoesNotExist:
        return JsonResponse({'error': 'File does not exist'}, status=404)

def list_uploaded_files(request):
    files = UploadedFile.objects.all().values('id', 'file_name', 'uploaded_at')
    print(files)
    return JsonResponse(list(files), safe=False)


def file_upload_success(request):
    return HttpResponse("File uploaded successfully!")