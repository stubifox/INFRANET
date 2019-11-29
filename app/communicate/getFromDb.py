"""
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:50:09
 * @modify date 2019-11-28 22:50:09
 * @desc [description]
"""
# getFromDb.py

import sqlite3
import sys
import os
import dataBaseConnection as dbCon
import json
from shared import Action, DictIndex


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
              FROM (
                SELECT * 
                FROM message_log AS log
                ORDER BY log.id DESC
                LIMIT 20 
              ) ORDER BY id ASC
          '''
    cursor.execute(sql)
    initData = cursor.fetchall()
    print(json.dumps(initData))
    con.close()


def getInsertedValue():
    con = dbCon.connectDb()
    con.row_factory = json_factory
    cursor = con.cursor()
    sql = '''SELECT * 
             FROM message_log AS log 
             ORDER BY log.id desc
             LIMIT 1
           '''
    cursor.execute(sql)
    lastEntry = cursor.fetchall()
    print(json.dumps(lastEntry))
    con.close()


def loadMoreEntrys(startID):
    con = dbCon.connectDb()
    con.row_factory = json_factory
    cursor = con.cursor()

    sql = '''   SELECT * FROM (
                    SELECT * 
                    FROM message_log AS log
                    WHERE log.id < ?
                    ORDER BY id DESC
                    LIMIT 20)
                ORDER BY id ASC
          '''
    cursor.execute(sql, (startID,))
    newEntrys = cursor.fetchall()
    print(json.dumps(newEntrys))
    con.close()


def main():
    load = dbCon.read_in_stdin()
    exp = load[DictIndex.LOAD.value]

    if exp == Action.INITIAL.value:
        getInitialLoad()
    elif exp == Action.ENTRY.value:
        getInsertedValue()
    elif exp == Action.LOAD_MORE.value:
        startID = load[DictIndex.ID.value]
        loadMoreEntrys(startID=startID)


if __name__ == '__main__':
    main()
