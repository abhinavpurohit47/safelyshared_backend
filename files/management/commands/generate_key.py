from django.core.management.base import BaseCommand
from files.models import EncryptionKey
import os

class Command(BaseCommand):
    help = 'Generate and store an AES-256 key'

    def handle(self, *args, **kwargs):
        key_name = 'aes_key'
        key_value = os.urandom(32)

        EncryptionKey.objects.create(key_name=key_name, key_value=key_value)
        self.stdout.write(self.style.SUCCESS('Successfully generated and stored AES-256 key'))