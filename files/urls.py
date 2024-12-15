from django.urls import path
from .views import FileUploadView, FileListView
from .views import upload_file, file_upload_success, download_file, list_uploaded_files, delete_file, generate_download_link, download_file_signed
# urlpatterns = [
#     path('upload/', FileUploadView.as_view(), name='file-upload'),
#     path('files/', FileListView.as_view(), name='file-list'),
# ]

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('upload/success/', file_upload_success, name='file_upload_success'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('files/', list_uploaded_files, name='list_uploaded_files'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('generate-download-link/<int:file_id>/', generate_download_link, name='generate_download_link'),
    path('download-signed/', download_file_signed, name='download_file_signed'),
]