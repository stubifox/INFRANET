"""
 * @author Fabian Galefski
 * @email fabian.galefski@gmail.com
 * @create date 2019-11-29 12:00:00
 * @modify date 2019-12-04 23:40:00
 * @desc [description]
"""

# transferFrontBack.py
import sys
import sqlite3
import os
import json
from multiprocessing.connection import Client
from helperClasses import DataBaseUtilities, UniversalUtilities
from shared import DictIndex, Action


# fuction for requesting the arduino state from an port 6000
def requestState():
    try:
        address = ('localhost', 6000)
        conn = Client(address, authkey=b'PyToPyCom')
        # status, if an local arduino is connected
        localArdState = str(conn.send('ArdConState'))
        # status, if an arduino is connected by infrared
        externalArdState = str(conn.send('CommunicationState'))
        partnerID = str(conn.send('PartnerID'))
        conn.send('finished')
        conn.close()
        return localArdState, externalArdState, partnerID
    except ConnectionError as e:
        UniversalUtilities.sendErrorMessageToFrontend(e)

# function to verify if there are new messages since the last refresh of the frontend and to return these new Messages


def databaseState(lastMessageId, partnerID):
    sql = '''SELECT log.id
             FROM message_log AS log 
             ORDER BY log.id desc
             LIMIT 1
           '''
    newMessageId = DataBaseUtilities.getOneValueFromDb(
        sql)  # newest message-id in the database
    # calculate how many messages arrived since the last refresh of the frontend
    counterNewMessages = newMessageId['id'] - lastMessageId
    if counterNewMessages > 0:  # returns the messages, which arrived since the last refresh of the frontend
        sql = ''' SELECT *
              FROM (
                SELECT *
                FROM message_log AS log 
                ORDER BY log.id desc
                LIMIT ?
                WHERE partner_id = ?
              ) ORDER BY id ASC
          '''
        newData = DataBaseUtilities.getValuesFromDb(
            sql, counterNewMessages, partnerID)
        return True, newData
    else:
        return False, None

# build json for the frontend withe the arduino states and the new messages


def jsonFrontEnd(ardLoc, ardExt, partnerID, newMessagesInDb, messages):
    print(json.dumps({DictIndex.LOCAL_ARDUINO_STATE.value: ardLoc,
                      DictIndex.EXTERNAL_ARDUINO_STATE.value: ardExt,
                      DictIndex.PARTNER_ID: partnerID,
                      DictIndex.SHOULD_UPDATE_MESSAGES.value: newMessagesInDb,
                      DictIndex.NEW_MESSAGES.value: messages}))

# main


def main():

    load = UniversalUtilities.read_in_stdin_json()
    exp = load[DictIndex.LOAD.value]

    if exp == Action.INITIAL.value:
        try:
            ardLoc, ardExt, _ = requestState()
            jsonFrontEnd(ardLoc, ardExt, None, None, None)
        except ConnectionError as e:
            UniversalUtilities.sendErrorMessageToFrontend(e)
    elif exp == Action.ID.value:
        lastId = load[DictIndex.ID.value]
        try:
            ardLoc, ardExt, partnerID = requestState()
            newMessagesInDb, messages = databaseState(lastId, partnerID)
            jsonFrontEnd(ardLoc, ardExt, partnerID, newMessagesInDb, messages)
        except ConnectionError as e:
            UniversalUtilities.sendErrorMessageToFrontend(e)
        except sqlite3.Error as e:
            UniversalUtilities.sendErrorMessageToFrontend(e)


if __name__ == '__main__':
    main()
