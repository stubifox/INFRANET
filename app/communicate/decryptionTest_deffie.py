from diffiehellman.diffiehellman import DiffieHellman
from cryptography.fernet import Fernet
from hashlib import blake2b
import json
import struct
import base64


def encryptAndDecryptMessage(message):
    '''This file/method only exists for testing porposes'''
    sender = DiffieHellman(group=5)
    recipient = DiffieHellman(group=5)

    sender.generate_public_key()
    recipient.generate_public_key()
    print("length of public key", len(str(sender.public_key)))
    print("public key", sender.public_key)

    sender.generate_shared_secret(recipient.public_key)
    recipient.generate_shared_secret(sender.public_key)

    # SENDER SIDE
    blakeSender = blake2b(digest_size=16)
    blakeSender.update(sender.shared_key.encode())
    fernetSender = Fernet(base64.urlsafe_b64encode(
        blakeSender.hexdigest().encode()))
    encryptedMessage = fernetSender.encrypt(json.dumps(message).encode())
    print("length of encrytped message", len(str(encryptedMessage)))

    # RECIPIENT SIDE
    blakeRecipient = blake2b(digest_size=16)
    blakeRecipient.update(recipient.shared_key.encode())
    fernetRecipient = Fernet(base64.urlsafe_b64encode(
        blakeRecipient.hexdigest().encode()))
    decryptedMessage = fernetRecipient.decrypt(encryptedMessage)
    print("decrypted decoded message", decryptedMessage.decode())


message = "Great and wonderful message about some important security stuff"
encryptAndDecryptMessage(message)
