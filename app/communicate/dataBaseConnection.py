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
import decryptionTest

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


def createSettingsTable():
    con = connectDb()
    dbcursor = con.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    ) '''
    dbcursor.execute(sql)
    con.commit()
    con.close()


def createDataBase():
    con = connectDb()
    dbcursor = con.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS message_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        sender TEXT NOT NULL,
        time TEXT NOT NULL,
        date TEXT NOT NULL,
        message TEXT NOT NULL
    ) '''

    dbcursor.execute(sql)
    con.commit()
    con.close()


def insertToDb(sender, message,):
    con = connectDb()
    dbcursor = con.cursor()
    sql = '''INSERT INTO message_log (sender, time, date, message)
        VALUES(?, time('now', 'localtime'), date('now'), ?)'''
    dbcursor.execute(sql, (sender, message))
    con.commit()
    con.close()


def main():
    data = read_in_stdin()
    if data[DictIndex.LOAD.value] == Action.INITIAL.value:
        createDataBase()
        createSettingsTable()
        return
    elif data[DictIndex.LOAD.value] == Action.INSERT.value:
        message, sender = data[DictIndex.MESSAGE.value], data[DictIndex.SENDER.value]
        insertToDb(sender=sender, message=message)



if __name__ == '__main__':
    main()
