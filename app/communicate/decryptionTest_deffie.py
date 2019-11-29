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
    recipient.generate_shared_secret(sender.public_key)

    message = "very great secret message from sender <3"

    # SENDER SIDE
    blakeSender = blake2b(digest_size=16)
    blakeSender.update(sender.shared_key.encode())
    fernetSender = Fernet(base64.urlsafe_b64encode(blakeSender.hexdigest().encode()))
    encryptedMessage = fernetSender.encrypt(message.encode())

    # RECIPIENT SITE
    blakeRecipient = blake2b(digest_size=16)
    blakeRecipient.update(recipient.shared_key.encode())
    fernetRecipient = Fernet(base64.urlsafe_b64encode(blakeRecipient.hexdigest().encode()))
    decryptedMessage = fernetRecipient.decrypt(encryptedMessage)
    print(decryptedMessage.decode())

    print("-----------------------------SENDER SHARED KEY AS BYTES")
    print(blake.hexdigest())
    print(len(blake.hexdigest()))
    fernet = Fernet(base64.urlsafe_b64encode(blake.hexdigest().encode()))
