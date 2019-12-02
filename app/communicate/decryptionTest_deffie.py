from diffiehellman.diffiehellman import DiffieHellman
from cryptography.fernet import Fernet
from hashlib import blake2b
import json
import struct
import base64

def encryptAndDecryptMessage(message):

    sender = DiffieHellman()
    recipient = DiffieHellman()

    sender.generate_public_key()
    recipient.generate_public_key()

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
    print(encryptedMessage)


    # RECIPIENT SITE
    blakeRecipient = blake2b(digest_size=16)
    blakeRecipient.update(recipient.shared_key.encode())
    fernetRecipient = Fernet(base64.urlsafe_b64encode(blakeRecipient.hexdigest().encode()))
    decryptedMessage = fernetRecipient.decrypt(encryptedMessage)
    print(decryptedMessage.decode())

encryptAndDecryptMessage("Great message from our sponsor BEST MOBILE GAME EVAAA")