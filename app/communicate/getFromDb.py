import sqlite3
import sys
import os
import dataBaseConnection as dbCon
import json


def json_factory(cursor, row):
    json = {}
    for idx, col in enumerate(cursor.description):
        json[col[0]] = row[idx]
    return json


def getValuesFromDb():
    con = dbCon.connectDb()
    con.row_factory = json_factory
    dbcursor = con.cursor()
    dbcursor.execute('''SELECT * FROM message_log''')
    data = dbcursor.fetchall()
    print(json.dumps(data))
    con.close()


def main():
    getValuesFromDb()


if __name__ == '__main__':
    main()
