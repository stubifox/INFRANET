from diffiehellman.diffiehellman import DiffieHellman
from cryptography.fernet import Fernet
from hashlib import blake2b
import json
import struct
import base64

def encryptAndDecryptMessage(message):
    '''This file/method only exists for testing porposes'''
    sender = DiffieHellman(key_length=200, group=5)
    recipient = DiffieHellman(key_length=200, group=5)

    sender.generate_public_key()
    recipient.generate_public_key()
    print("length of public key",len(hex(sender.public_key)))
    print("public key", hex(sender.public_key))

    sender.generate_shared_secret(recipient.public_key)
    recipient.generate_shared_secret(sender.public_key)

    # message = {
    #     "message": "HEEEY WASSS UP HIER MEINE FINANZDATEN LG qwertzuioasdfghjk",
    #     "sender": "qwertzuioasdfghjk"
    # }

    # SENDER SIDE
    blakeSender = blake2b(digest_size=16)
    blakeSender.update(sender.shared_key.encode())
    fernetSender = Fernet(base64.urlsafe_b64encode(blakeSender.hexdigest().encode()))
    encryptedMessage = fernetSender.encrypt(json.dumps(message).encode())
    print("length of encrytped message",len(encryptedMessage))


    # RECIPIENT SIDE
    blakeRecipient = blake2b(digest_size=16)
    blakeRecipient.update(recipient.shared_key.encode())
    fernetRecipient = Fernet(base64.urlsafe_b64encode(blakeRecipient.hexdigest().encode()))
    decryptedMessage = fernetRecipient.decrypt(encryptedMessage)
    print("decrypted decoded message" ,decryptedMessage.decode())

message = "pxhEp11wCghyhAMNA0duZn0FpctQOR53jlDKuOOtlyoGMTO7QHmRaavCFX2YOUZnFhocyD78P5XTKJSxzG5v76pAliKvz3S9r47S8v4woHSzXbifw5T7DVUbXwQYv2F8pcLU7NBwUg58rsGA4NzdDWE81pVIY6r9SG2uh83fK4142Enf479GnD4chlfKlB003wlx66ZYPGRGM3wQJk8igB0AJZdRBEU3QI1pnv2GtnMmoqlPJ4xJD5RJh3DLHaG7ekyjO612RQIBu11h0rwkxWaa"
print(len(message))
encryptAndDecryptMessage(message)