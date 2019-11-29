from diffiehellman.diffiehellman import DiffieHellman
from cryptography.fernet import Fernet
from hashlib import blake2b
import json
import struct
import base64

def encryptAndDecryptMessage():

    sender = DiffieHellman()
    recipient = DiffieHellman()

    sender.generate_public_key()
    recipient.generate_public_key()

    sender.generate_shared_secret(recipient.public_key)

    print("-----------------------------SENDER SHARED KEY")
    print(sender.shared_key)
    print("-----------------------------SENDER SHARED SECRET")
    print(sender.shared_secret)

    key = Fernet.generate_key
    print("-----------------------------FERNET KEY")
    print(str(key))

    blake = blake2b(digest_size=16)
    blake.update(sender.shared_key.encode())

    print("-----------------------------SENDER SHARED KEY AS BYTES")
    print(blake.hexdigest())
    print(len(blake.hexdigest()))
    fernet = Fernet(base64.urlsafe_b64encode(blake.hexdigest().encode()))
