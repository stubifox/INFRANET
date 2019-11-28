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
    if data['load'] == 'initial':
        createDataBase()
        createSettingsTable()
        return
    else:
        #! data muss immer von der Form sein: {"message": "...", "sender": "..."}!, wird aber im frontend behandelt
        message, sender = data['message'], data['sender']
        insertToDb(sender=sender, message=message)


if __name__ == '__main__':
    main()
