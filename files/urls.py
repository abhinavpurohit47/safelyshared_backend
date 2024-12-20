from django.urls import path
from .views import FileUploadView, FileDownloadView, file_upload_success,get_aes_view, download_file,get_encryption_key, list_uploaded_files, delete_file, generate_download_link, download_file_signed

urlpatterns = [
    path('get_aes/', get_aes_view, name='get_aes'),
     path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('upload/success/', file_upload_success, name='file_upload_success'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('files/', list_uploaded_files, name='list_uploaded_files'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    path('generate-download-link/<int:file_id>/', generate_download_link, name='generate_download_link'),
    path('download-signed/', download_file_signed, name='download_file_signed'),
    path('api/get_encryption_key/', get_encryption_key, name='get_encryption_key'),
]