from diffiehellman.diffiehellman import DiffieHellman
from cryptography.fernet import Fernet
from hashlib import blake2b
import json
import sqlite3
import getFromDb
import dataBaseConnection
import jsonpickle
import base64

class encryptionHandler:
    
    def createAndSaveEncryptionKeys(self):
        keyHandler = DiffieHellman()
        keyHandler.generate_public_key()
        
        self._insertKeyHandlerIntoDb(keyHandler)

    def createAndSaveSharedSecret(self, foreignPublicKey):
        '''Takes a public key from someone else and generates a sharedSecret'''
        keyHandler = self._getKeyHandlerJsonFromDb()
        keyHandler.generate_shared_secret(foreignPublicKey)
        self._insertKeyHandlerIntoDb(keyHandler)

    def encryptString(self, stringToEncrypt):
        keyHandler = self._getKeyHandlerJsonFromDb()
        blake = blake2b(digest_size=16)
        blake.update(keyHandler.shared_key.encode())
        fernet = Fernet(base64.urlsafe_b64encode(blake.hexdigest().encode()))
        return fernet.encrypt(json.dumps(stringToEncrypt).encode())

    def decryptByteArray(self, encryptedByteArray):
        keyHandler = self._getKeyHandlerJsonFromDb()
        blake = blake2b(digest_size=16)
        blake.update(keyHandler.shared_key.encode())
        fernet = Fernet(base64.urlsafe_b64encode(blake.hexdigest().encode()))
        return json.loads(fernet.decrypt(encryptedByteArray))

    def _insertKeyHandlerIntoDb(self, keyHandler):
        '''Encodes a DiffieHellman class as JSON and saves it as a string in the settings table'''
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
        keyHandlerJson = cursor.fetchall()
        return jsonpickle.decode(keyHandlerJson[0]["value"])

# keyHandler2 = DiffieHellman()
# keyHandler2.generate_public_key()

# createAndSaveEncryptionKeys()
# createAndSaveSharedSecret(keyHandler2.public_key)
# message = { "message": "HEEEY WASSS UP HIER MEINE FINANZDATEN LG qwertzuioasdfghjk", "sender": "qwertzuioasdfghjk" }
# encryptedMessage = encryptString(message)
# print(encryptedMessage)
# print(decryptByteArray(encryptedMessage))
