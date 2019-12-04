from diffiehellman.diffiehellman import DiffieHellman, MalformedPublicKey
from cryptography.fernet import Fernet, InvalidToken
from hashlib import blake2b
import json
import sqlite3
import getFromDb
import dataBaseConnection
import jsonpickle
import base64
from helperClasses import DataBaseUtilities, UniversalUtilities


class EncryptionHandler:

    def createAndSaveSharedSecret(self, foreignPublicKey):
        '''Takes a public key from someone else and generates a sharedSecret'''
        keyHandler = self._getKeyHandlerFromDb()
        try:
            keyHandler.generate_shared_secret(foreignPublicKey)
        except MalformedPublicKey as e:
            UniversalUtilities.sendErrorMessageToFrontend(e)
        self._insertKeyHandlerIntoDb(keyHandler)

    def encryptString(self, stringToEncrypt):
        '''TReturns void if the encryption fails'''
        keyHandler = self._getKeyHandlerFromDb()
        blake = blake2b(digest_size=16)
        try:
            blake.update(keyHandler.shared_key.encode())
            fernet = Fernet(base64.urlsafe_b64encode(
                blake.hexdigest().encode()))
            # auf länge cappen (max 511 bytes) warten auf Kai
            return fernet.encrypt(json.dumps(stringToEncrypt).encode())
        except AttributeError as e:
            UniversalUtilities.sendErrorMessageToFrontend(e)
            return None
        except InvalidToken as e:
            UniversalUtilities.sendErrorMessageToFrontend(e)
            return None

    def decryptByteArray(self, encryptedByteArray):
        '''Returns void if the decryption fails'''
        keyHandler = self._getKeyHandlerFromDb()
        blake = blake2b(digest_size=16)
        try:
            blake.update(keyHandler.shared_key.encode())
            fernet = Fernet(base64.urlsafe_b64encode(
                blake.hexdigest().encode()))
            return json.loads(fernet.decrypt(encryptedByteArray))
        except AttributeError as e:
            UniversalUtilities.sendErrorMessageToFrontend(e)
            return None
        except InvalidToken as e:
            UniversalUtilities.sendErrorMessageToFrontend(e)
            return None

    def getLocalPublicKey(self):
        '''Returns the local public_key as string'''
        keyHandler = self._getKeyHandlerFromDb()
        return str(keyHandler.public_key)

    def _createAndSaveEncryptionKeys(self):
        keyHandler = DiffieHellman(key_length=200, group=5)
        keyHandler.generate_public_key()
        self._insertKeyHandlerIntoDb(keyHandler)
        return keyHandler

    def _insertKeyHandlerIntoDb(self, keyHandler):
        '''Encodes a DiffieHellman class as JSON and saves it as a string into settings table'''
        keyHandlerJson = jsonpickle.encode(keyHandler)
        statement = '''INSERT OR REPLACE INTO settings (key, value) VALUES('keyHandlerJson', ?)'''
        DataBaseUtilities.insertIntoDb(statement, keyHandlerJson)

    def _getKeyHandlerFromDb(self):
        '''Fetches the DiffieHellman JSON from the settings table and returns the decoded class'''
        statement = ''' SELECT value FROM settings WHERE key = 'keyHandlerJson' '''
        results = DataBaseUtilities.getValuesFromDb(statement)
        if len(results) == 0:
            return self._createAndSaveEncryptionKeys()
        return jsonpickle.decode(results[0]["value"])
