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
from helperClasses import UniversalUtilities, DataBaseUtilities

# deprecated BEGIN


def json_factory(cursor, row):
    sqliteJson = {}
    for idx, col in enumerate(cursor.description):
        sqliteJson[col[0]] = row[idx]
    return sqliteJson

# deprecated END


def getInitialLoad():
    sql = ''' SELECT *
            FROM (
            SELECT * 
            FROM message_log AS log
            ORDER BY log.id DESC
            LIMIT 20 
            ) ORDER BY id ASC
        '''
    DataBaseUtilities.sendDataToFrontendFromDb(sqlStatement=sql)


def getInsertedValue():
    sql = '''SELECT * 
             FROM message_log AS log 
             ORDER BY log.id desc
             LIMIT 1
           '''
    DataBaseUtilities.sendDataToFrontendFromDb(sqlStatement=sql)


def loadMoreEntrys(startID):
    sql = '''   SELECT * FROM (
                    SELECT * 
                    FROM message_log AS log
                    WHERE log.id < ?
                    ORDER BY id DESC
                    LIMIT 20)
                ORDER BY id ASC
          '''
    DataBaseUtilities.sendDataToFrontendFromDb(sql, startID)


def main():
    load = UniversalUtilities.read_in_stdin_json()
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
