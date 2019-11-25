from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import json

def encryptAndDecryptMessage(data):
    password_input = "testString"
    password = password_input.encode()
    salt = b's3cr3ts4lt'
    kdf1 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf1.derive(password))

    kdf2 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key2 = base64.urlsafe_b64encode(kdf2.derive(password))

    encrypted = Fernet(key).encrypt(data.encode())
    x = {
        "message": str(encrypted.decode())
    }
    print(json.dumps(x))

    decrypted = Fernet(key2).decrypt(encrypted)
    y = {
        "message": str(decrypted.decode())
    }
    print(json.dumps(y))