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


def getInitialLoad():
    con = dbCon.connectDb()
    con.row_factory = json_factory
    cursor = con.cursor()
    sql = ''' SELECT *
              FROM message_log
              WHERE id BETWEEN (SELECT max(id)
              FROM message_log) - 20 
              AND (SELECT max(id)
              FROM message_log)
          '''
    cursor.execute(sql)
    initData = cursor.fetchall()
    print(json.dumps(initData))
    con.close()


def getInsertedValue():
    con = dbCon.connectDb()
    con.row_factory = json_factory
    cursor = con.cursor()
    sql = '''SELECT * FROM message_log AS log 
        WHERE log.id = (SELECT max(id) FROM message_log)'''
    cursor.execute(sql)
    lastEntry = cursor.fetchall()
    print(json.dumps(lastEntry))


def loadMoreEntrys(startID):
    con = dbCon.connectDb()
    con.row_factory = json_factory
    cursor = con.cursor()
    sql = '''SELECT * FROM  message_log AS log
            WHERE log.id BETWEEN ? - 20 AND ?'''
    cursor.execute(sql, (startID, startID))
    newEntrys = cursor.fetchall()
    print(json.dumps(newEntrys))


def main():
    load = dbCon.read_in_stdin()
    exp = load['load']

    if exp == 'initial':
        getInitialLoad()
    elif exp == 'entry':
        getInsertedValue()
    elif exp == 'loadMore':
        startID = load['id']
        loadMoreEntrys(startID - 1)


if __name__ == '__main__':
    main()
