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


# deprecated BEGIN
path = os.path.join(os.path.dirname(__file__), '..',
                    '..',  'Log', 'chatLog.db')


def connectDb():
    try:
        con = sqlite3.connect(path)
        return con
    except sqlite3.Error as e:
        print(e)


def read_in_stdin():
    return json.loads(sys.stdin.readline())

# deprecated END


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


def insertMessageAndSender(sender, message):
    sql = '''INSERT INTO message_log (sender, time, date, message)
        VALUES(?, time('now', 'localtime'), date('now'), ?)'''
    DataBaseUtilities.insertIntoDb(sql, sender, message)


def main():
    data = UniversalUtilities.read_in_stdin_json()
    if data[DictIndex.LOAD.value] == Action.INITIAL.value:
        createDataBase()
        createSettingsTable()
        return
    elif data[DictIndex.LOAD.value] == Action.INSERT.value:
        message, sender = data[DictIndex.MESSAGE.value], data[DictIndex.SENDER.value]
        insertMessageAndSender(sender=sender, message=message)


if __name__ == '__main__':
    main()
