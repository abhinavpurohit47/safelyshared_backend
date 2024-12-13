from django.db import models

class SharedFile(models.Model):
    file = models.FileField(upload_to='shared_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

# class UploadedFile(models.Model):
#     file = models.FileField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)


class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    encrypted_content = models.TextField(default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class EncryptionKey(models.Model):
    key_name = models.CharField(max_length=255, unique=True)
    key_value = models.BinaryField()