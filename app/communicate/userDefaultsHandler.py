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
import uuid as guid


def getUUIDFromSettings():
    sql = '''SELECT value FROM settings WHERE key='uuid' '''
    return DataBaseUtilities.getOneValueFromDb(sqlStatement=sql)


def getThemeFromSettings():
    sql = '''SELECT value FROM settings WHERE key='theme' '''
    return DataBaseUtilities.getOneValueFromDb(sqlStatement=sql)


def insertDefaults(uuid, theme):
    sqlInsert = '''INSERT OR REPLACE INTO settings (key, value)
        VALUES('uuid', ?), ('theme', ?)'''
    DataBaseUtilities.insertIntoDb(sqlInsert, str(uuid), str(theme))


def insertThemeOnly(theme):
    sqlInsert = '''INSERT OR REPLACE INTO settings (key, value)
        VALUES('theme', ?)'''
    DataBaseUtilities.insertIntoDb(sqlInsert, str(theme))


def sendDefaults():
    sql = '''SELECT * FROM settings'''
    DataBaseUtilities.sendDataToFrontendFromDb(sqlStatement=sql)


def main():
    # try:
    inputData = UniversalUtilities.read_in_stdin_json()
    theme = inputData[DictIndex.THEME.value]
    if inputData[DictIndex.LOAD.value] == Action.CHECK.value:
        settings_uuid = getUUIDFromSettings()
        if settings_uuid == None:
            insertDefaults(uuid=guid.uuid4(), theme=theme)
        sendDefaults()
    if inputData[DictIndex.LOAD.value] == Action.UPDATE_THEME.value:
        insertThemeOnly(theme=theme)
    # except Exception as e:
    #     UniversalUtilities.sendErrorMessageToFrontend(e)


if __name__ == "__main__":
    main()
