"""
 * @author Fabian Galefski
 * @email fabian.galefski@gmail.com
 * @create date 2019-11-29 12:00:00
 * @modify date 2019-12-04 21:40:00
 * @desc [description]
"""

# transferFrontBack.py
import sys
import sqlite3
import os
import json
import helperClasses as helper
import dataBaseConnection as dbCon
from multiprocessing.connection import Client
from getFromDb import json_factory


#fuction for requesting the arduino state from an external script
def requestState():
    address = ('localhost',6000)
    conn = Client(address, authkey = b'PytoPyCom')
    localArdState = str(conn.send('ArdConState'))
    externalArdState = str(conn.send('CommunicationState'))
    conn.close()
    return localArdState, externalArdState

#function to request the last 20 messages stored in the database
def databaseState(lastMessageId):
    con = dbCon.connectDb()
    con.row_factory = json_factory
    cursor = con.cursor()
    sql = '''SELECT log.id
             FROM message_log AS log 
             ORDER BY log.id desc
             LIMIT 1
           '''
    cursor.execute(sql)
    newMessageId = cursor.fetchone()#fetchone

    print('Ausgabe')
    print(newMessageId)
    print(newMessageId['id'])
    print('Ende Ausgabe')

    #aus array id zurück in newMessageId
    counterNewMessages = newMessageId['id']-lastMessageId

    #print('counterNewMessages')
    #print(counterNewMessages)

    if counterNewMessages > 0:
        
        sql = ''' SELECT *
              FROM (
                SELECT *
                FROM message_log AS log 
                ORDER BY log.id desc
                LIMIT ?
              ) ORDER BY id ASC
          '''#doppeltes Select-Statement
        cursor.execute(sql,(counterNewMessages,))
        newData = cursor.fetchall()
        con.close()

        print(newData)

        return newData
    else:
        return 'Messages up to date'

#return json for the frontend
def jsonFrontEnd(ardLoc, ardExt, datMess):
    return json.dumps({'LocalArduinoState': ardLoc, 'ExternalArduinoState': ardExt, 'databaseMessageState': datMess })

#main
def main():
    #ardLoc, ardExt = 'True', 'True'
    ardLoc, ardExt = requestState()
    datMess = databaseState(5)          #Übergabewert ist die letzte Id des Frontends hier die 5
    #print('\nRueckgabe Datenbank\n')
    #print(datMess)
    #print('\nJson bauen\n')
    print(jsonFrontEnd(ardLoc, ardExt, datMess))
        
    

if __name__ == '__main__':
    main()

    
#function to verify if there were changes of the state of the arduinos
#def arduinoStateChanged():
#    localArdState, externalArdState = requestState()
#    if localArdState == 'False' and externalArdState == 'False':
#        return 'False', 'False'
#    elif localArdState == 'True' and externalArdState == 'False':
#        return localArdState, 'False'
#    elif localArdState == 'False' and externalArdState == 'True':
#       return 'False', externalArdState
#    else:
#        return localArdState, externalArdState


#function to verify if there were changes since the last message, message compared to lasat message from frontend
#def databaseMessageStateChanged(lastMessageId):
#    lastMessageIdDecoded = json.loads(lastMessageId)
#    newMessageState = databaseState(lastMessageIdDecoded)
#    if newMessageState != lastMessageIdDecoded:
#        return 'True'
#    else:
#        return 'False'