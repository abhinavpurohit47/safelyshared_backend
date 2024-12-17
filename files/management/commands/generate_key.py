from django.core.management.base import BaseCommand
from files.models import EncryptionKey
from Crypto.Random import get_random_bytes

class Command(BaseCommand):
    help = 'Generate and store AES key'

    def handle(self, *args, **kwargs):
        key_name = 'aes_key'
        key_value = get_random_bytes(32)

        if not EncryptionKey.objects.filter(key_name=key_name).exists():
            EncryptionKey.objects.create(key_name=key_name, key_value=key_value)
            self.stdout.write(self.style.SUCCESS('Successfully created AES key'))
        else:
            self.stdout.write(self.style.WARNING('AES key already exists'))