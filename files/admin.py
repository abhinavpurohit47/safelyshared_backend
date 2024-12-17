from django.core.management.base import BaseCommand
from files.models import EncryptionKey
import os

class Command(BaseCommand):
    help = 'Add AES encryption key to the database'

    def handle(self, *args, **kwargs):
        key_name = 'aes_key'
        key_value = os.urandom(32)

        if not EncryptionKey.objects.filter(key_name=key_name).exists():
            EncryptionKey.objects.create(key_name=key_name, key_value=key_value)
            self.stdout.write(self.style.SUCCESS('Successfully added AES key to the database'))
        else:
            self.stdout.write(self.style.WARNING('AES key already exists in the database'))