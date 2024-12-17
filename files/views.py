import base64
import mimetypes
from urllib.parse import urlencode
from django.http import Http404, HttpResponse
from rest_framework import generics
from .models import EncryptionKey, SharedFile
# from .serializers import SharedFileSerializer
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
from django.core.signing import Signer, TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings
from django.views.decorators.http import require_GET
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from .encryption import encrypt_file_content, decrypt_file_content, get_aes_key
# class FileUploadView(generics.CreateAPIView):
#     queryset = SharedFile.objects.all()
#     serializer_class = SharedFileSerializer

# class FileListView(generics.ListAPIView):
#     queryset = SharedFile.objects.all()
#     serializer_class = SharedFileSerializer
class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file_name = request.data.get('file_name')
        encrypted_content = base64.b64decode(request.data.get('encrypted_content'))
        iv = base64.b64decode(request.data.get('iv'))

        uploaded_file = UploadedFile(
            file_name=file_name,
            encrypted_content=encrypted_content,
            iv=iv
        )
        uploaded_file.save()

        return Response({'message': 'File uploaded successfully'}, status=201)

signer = TimestampSigner()
def home(request):
    return HttpResponse("Welcome to the Home Page")
class FileDownloadView(APIView):
    def get(self, request, file_id, *args, **kwargs):
        try:
            uploaded_file = UploadedFile.objects.get(id=file_id)
            key = get_aes_key()
            decrypted_content = decrypt_file_content(
                uploaded_file.encrypted_content,
                uploaded_file.iv,
                key
            )
            response = HttpResponse(decrypted_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file_name}"'
            return response
        except UploadedFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
def upload_file(request):
    file_name = request.data.get('file_name')
    encrypted_content = base64.b64decode(request.data.get('encrypted_content'))
    iv = base64.b64decode(request.data.get('iv'))

    uploaded_file = UploadedFile(
        file_name=file_name,
        encrypted_content=encrypted_content,
        iv=iv
    )
    uploaded_file.save()

    return Response({'message': 'File uploaded successfully'}, status=201)

def get_aes_view(request):
    try:
        key = get_aes_key()
        key_hex = key.hex()
        print(key_hex, 'KEY54')
        return JsonResponse({'key': key_hex})
    except EncryptionKey.DoesNotExist:
        return JsonResponse({'error': 'Encryption key not found'}, status=404)
    
def download_file(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        raise Http404("File does not exist")

    aes_key = get_aes_key()
    iv = uploaded_file.iv[:16]

    response_data = {
        'iv': iv.hex(),
        'encrypted_content': uploaded_file.encrypted_content.hex(),
        'file_name': uploaded_file.file_name
    }
    return JsonResponse(response_data)
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
    iv = uploaded_file.iv[:16]  # Ensure the IV is a string or bytes
    print(iv, 'IV')  # Debugging print statement

    if isinstance(iv, str):
        iv = bytes.fromhex(iv)  # Convert hex string to bytes
    elif isinstance(iv, bytes):
        iv = iv[:16]  # Ensure the IV is 16 bytes long

    if len(iv) != 16:
        return HttpResponse('Incorrect IV length', status=400)

    # decrypted_content = decrypt_file_content(uploaded_file.encrypted_content, aes_key, iv)
    response_data = {
        'iv': iv.hex(),
        'encrypted_content': uploaded_file.encrypted_content.hex(),
        'file_name': uploaded_file.file_name
    }

    response = HttpResponse(response_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file_name}"'
    return response
def generate_download_link(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        raise Http404("File does not exist")

    signed_value = signer.sign(file_id)
    download_url = request.build_absolute_uri(reverse('download_file_signed') + '?' + urlencode({'file_id': signed_value}))
    return JsonResponse({'download_url': download_url})


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

def get_encryption_key():
    try:
        key = EncryptionKey.objects.get(key_name='aes_key').key_value
        print(key, 'KEY')
        return JsonResponse({'key': key.hex()})
    except EncryptionKey.DoesNotExist:
        return JsonResponse({'error': 'Encryption key not found'}, status=404)