import base64
import mimetypes
from urllib.parse import urlencode
from django.http import Http404, HttpResponse
from rest_framework import generics
from .models import SharedFile
from .serializers import SharedFileSerializer
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
from django.core.signing import Signer, TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings
from django.urls import reverse
from .encryption import encrypt_file_content, decrypt_file_content, get_aes_key
class FileUploadView(generics.CreateAPIView):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer

class FileListView(generics.ListAPIView):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer


signer = TimestampSigner()
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

def generate_download_link(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        raise Http404("File does not exist")

    signed_value = signer.sign(file_id)
    download_url = request.build_absolute_uri(reverse('download_file_signed') + '?' + urlencode({'file_id': signed_value}))
    return JsonResponse({'download_url': download_url})

def download_file_signed(request):
    signed_file_id = request.GET.get('file_id')
    try:
        file_id = signer.unsign(signed_file_id, max_age=3600)
        uploaded_file = UploadedFile.objects.get(id=file_id)
    except (BadSignature, SignatureExpired):
        return HttpResponse('Invalid or expired download link', status=400)
    except UploadedFile.DoesNotExist:
        raise Http404("File does not exist")

    aes_key = get_aes_key()
    decrypted_content = decrypt_file_content(uploaded_file.encrypted_content, aes_key)
    mime_type, _ = mimetypes.guess_type(uploaded_file.file_name)
    response = HttpResponse(decrypted_content, content_type=mime_type or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file_name}"'
    return response


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