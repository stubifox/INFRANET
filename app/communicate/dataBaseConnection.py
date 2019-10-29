# dataBaseConncetion.py
import sqlite3
import sys
import os
import json

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
    if not os.path.exists(path):
        createDataBase()
    data = read_in_stdin()
    #! data muss immer von der Form sein: {"message": "...", "sender": "..."}!, wird aber im frontend behandelt
    message, sender = data['message'], data['sender']
    insertToDb(sender=sender, message=message)


if __name__ == '__main__':
    main()
