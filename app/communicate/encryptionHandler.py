from diffiehellman.diffiehellman import DiffieHellman,MalformedPublicKey
from cryptography.fernet import Fernet,InvalidToken
from hashlib import blake2b
import json
import sqlite3
import getFromDb
import dataBaseConnection
import jsonpickle
import base64

# darf ich die errors überhaupt printen oder wie mach ich das?
class EncryptionHandler:
    
    def createAndSaveSharedSecret(self, foreignPublicKey):
        '''Takes a public key from someone else and generates a sharedSecret'''
        keyHandler = self._getKeyHandlerJsonFromDb()
        try:
            keyHandler.generate_shared_secret(foreignPublicKey)
        except MalformedPublicKey:
            print("ERROR: Could not create shared_secret. Please ensure a correct transfered public_key")
        self._insertKeyHandlerIntoDb(keyHandler)

    def encryptString(self, stringToEncrypt):
        '''This method returns void if the encryption fails'''
        keyHandler = self._getKeyHandlerJsonFromDb()
        blake = blake2b(digest_size=16)
        try:
            blake.update(keyHandler.shared_key.encode())
            fernet = Fernet(base64.urlsafe_b64encode(blake.hexdigest().encode()))
            return fernet.encrypt(json.dumps(stringToEncrypt).encode())
        except AttributeError:
            print("ERROR: Could not encrypt String. Please create a shared_secret with the createAndSaveSharedSecret() method beforehand")
            return
        except InvalidToken:
            print("ERROR: Could not encrypt String. Please ensure a correct transfered public_key")
            return
        

    def decryptByteArray(self, encryptedByteArray):
        '''This method returns void if the decryption fails'''
        keyHandler = self._getKeyHandlerJsonFromDb()
        blake = blake2b(digest_size=16)
        try:
            blake.update(keyHandler.shared_key.encode())
            fernet = Fernet(base64.urlsafe_b64encode(blake.hexdigest().encode()))
            return json.loads(fernet.decrypt(encryptedByteArray))
        except AttributeError:
            print("ERROR: Please create a shared_secret with the createAndSaveSharedSecret() method beforehand")
            return
        except InvalidToken:
            print("ERROR: Please ensure a correct transfered public_key")
            return

    def _createAndSaveEncryptionKeys(self):
        keyHandler = DiffieHellman()
        keyHandler.generate_public_key()
        self._insertKeyHandlerIntoDb(keyHandler)
        return keyHandler

    def _insertKeyHandlerIntoDb(self, keyHandler):
        '''Encodes a DiffieHellman class as JSON and saves it as a string into settings table'''
        keyHandlerJson = jsonpickle.encode(keyHandler)
        connection = dataBaseConnection.connectDb()
        connection.row_factory = getFromDb.json_factory
        cursor = connection.cursor()
        statement = '''INSERT OR REPLACE INTO settings (key, value) VALUES('keyHandlerJson', ?)'''
        cursor.execute(statement, (keyHandlerJson,))
        connection.commit()
        connection.close()

    def _getKeyHandlerJsonFromDb(self):
        '''Fetches the DiffieHellman JSON from the settings table and returns the decoded class'''
        connection = dataBaseConnection.connectDb()
        connection.row_factory = getFromDb.json_factory
        cursor = connection.cursor()
        statement = ''' SELECT value FROM settings WHERE key = 'keyHandlerJson' '''
        cursor.execute(statement)
        results = cursor.fetchall()

        if len(results) == 0:
            return self._createAndSaveEncryptionKeys()
        return jsonpickle.decode(results[0]["value"])

# keyHandler2 = DiffieHellman()
# keyHandler2.generate_public_key()

# createAndSaveEncryptionKeys()
# createAndSaveSharedSecret(keyHandler2.public_key)
# message = { "message": "HEEEY WASSS UP HIER MEINE FINANZDATEN LG qwertzuioasdfghjk", "sender": "qwertzuioasdfghjk" }
# encryptedMessage = encryptString(message)
# print(encryptedMessage)
# print(decryptByteArray(encryptedMessage))

# encryptionHandler.createAndSaveSharedSecret(keyHandler2.public_key - 1) // raises MalformedPublicKey
# fernet.decrypt raises InvalidToken
