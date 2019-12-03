"""
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:50:24
 * @modify date 2019-11-28 22:50:24
 * @desc [description]
"""
import sqlite3
import json
import getFromDb
import dataBaseConnection as dbCon
from shared import Action, DictIndex
from helperClasses import DataBaseUtilities, UniversalUtilities


def getDefaultsFromSettingsTable():
    sql = '''SELECT * FROM settings'''
    DataBaseUtilities.sendDataToFrontendFromDb(sqlStatement=sql)


def insertDefaults(uuid, theme):
    sqlInsert = '''INSERT OR REPLACE INTO settings (key, value)
        VALUES('uuid', ?), ('theme', ?)'''
    DataBaseUtilities.insertIntoDb(sqlInsert, uuid, str(theme))


def main():
    try:
        inputData = dbCon.read_in_stdin()
        if inputData[DictIndex.LOAD.value] == Action.CHECK.value:
            getDefaultsFromSettingsTable()

        if inputData[DictIndex.LOAD.value] == Action.INSERT.value:
            uuid, theme = inputData[DictIndex.UUID.value], inputData[DictIndex.THEME.value]
            insertDefaults(uuid=uuid, theme=theme)
            getDefaultsFromSettingsTable()
    except Exception as e:
        pass

    return


if __name__ == "__main__":
    main()
