from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
from files.models import EncryptionKey
import os
def get_aes_key():
    try:
        key = EncryptionKey.objects.get(key_name='aes_key').key_value
        print(key, 'KEY')
        return key
    except EncryptionKey.DoesNotExist:
        raise ValueError("Encryption key does not exist in the database")

def decrypt_file_content(encrypted_content, key):
    encrypted_content = base64.b64decode(encrypted_content)
    iv = encrypted_content[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_content = decryptor.update(encrypted_content[16:]) + decryptor.finalize()
    return decrypted_content

def encrypt_file_content(content, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(content) + padder.finalize()
    encrypted_content = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_content).decode('utf-8')