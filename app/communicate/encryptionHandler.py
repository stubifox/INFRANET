from diffiehellman.diffiehellman import DiffieHellman
from cryptography.fernet import Fernet
from hashlib import blake2b
import json
import sqlite3
import getFromDb
import dataBaseConnection

def createAndSaveEncryptionKeys():

    keyHandler = DiffieHellman()
    keyHandler.generate_public_key()

    # get private key
    #
    # keyHandler.public_key = 21345678
    # keyHandlerJson = json.dumps(keyHandler.__dict__)
    # print(keyHandlerJson["_DiffieHellman__private_key"])
    # for element in keyHandlerJson:
    #     print(element)

def insertAllKeys(pirvateKey, publicKey, foreignPublicKey):
    connection = dataBaseConnection.connectDb()
    connection.row_factory = getFromDb.json_factory
    cursor = connection.cursor()
    statement = '''INSERT OR REPLACE INTO settings (key, value)
        VALUES('privateKey', ?), ('publicKey', ?), ('foreignPublicKey', ?) '''
    cursor.execute(statement, (pirvateKey, publicKey, foreignPublicKey))
