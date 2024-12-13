from django.urls import path
from .views import FileUploadView, FileListView
from .views import upload_file, file_upload_success, download_file
# urlpatterns = [
#     path('upload/', FileUploadView.as_view(), name='file-upload'),
#     path('files/', FileListView.as_view(), name='file-list'),
# ]

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('upload/success/', file_upload_success, name='file_upload_success'),
    path('download/<int:file_id>/', download_file, name='download_file'),
]