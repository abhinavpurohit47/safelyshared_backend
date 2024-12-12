from rest_framework import serializers
from .models import SharedFile

class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ['id', 'file', 'uploaded_at', 'description']