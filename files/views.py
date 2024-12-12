from django.http import HttpResponse
from rest_framework import generics
from .models import SharedFile
from .serializers import SharedFileSerializer
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile

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
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_upload_success')
    else:
        form = UploadFileForm()
    return render(request, 'files/upload.html', {'form': form})

def file_upload_success(request):
    return HttpResponse("File uploaded successfully!")