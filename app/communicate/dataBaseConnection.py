"""
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:49:49
 * @modify date 2019-11-28 22:49:49
 * @desc [description]
"""
# dataBaseConncetion.py

import sqlite3
import sys
import os
import json
import getFromDb
from shared import Action
from shared import DictIndex
from helperClasses import DataBaseUtilities, UniversalUtilities


def createSettingsTable():
    sql = '''CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    ) '''
    DataBaseUtilities.insertIntoDb(sqlInsertStatement=sql)


def createDataBase():
    sql = '''CREATE TABLE IF NOT EXISTS message_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        sender TEXT NOT NULL,
        time TEXT NOT NULL,
        date TEXT NOT NULL,
        message TEXT NOT NULL
    ) '''
    DataBaseUtilities.insertIntoDb(sqlInsertStatement=sql)

def main():
    data = UniversalUtilities.read_in_stdin_json()
    if data[DictIndex.LOAD.value] == Action.INITIAL.value:
        createDataBase()
        createSettingsTable()
    elif data[DictIndex.LOAD.value] == Action.INSERT.value:
        message, sender = data[DictIndex.MESSAGE.value], data[DictIndex.SENDER.value]
        DataBaseUtilities.insertMessageAndSender(sender=sender, message=message)
        # try:
        #     UniversalUtilities.connectAndSendTo_6200(message=message)
        # except ConnectionError as e:
        #     UniversalUtilities.sendErrorMessageToFrontend(e)


if __name__ == '__main__':
    main()
