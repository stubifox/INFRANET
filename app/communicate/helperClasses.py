"""
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:50:24
 * @modify date 2019-11-28 22:50:24
 * @desc [description]
"""
# helperClasses.js
import os.path as path
import json
import sqlite3
from shared import DictIndex
import sys
from inspect import getframeinfo, stack


class DataBaseUtilities:
    _pathToDb = path.join(path.dirname(__file__),
                          '..', '..',  'Log', 'chatLog.db')

    @staticmethod
    def _json_factory(cursor, row):
        sqliteJson = {}
        for idx, col in enumerate(cursor.description):
            sqliteJson[col[0]] = row[idx]
        return sqliteJson

    @staticmethod
    def dbConnection():
        try:
            con = sqlite3.connect(DataBaseUtilities._pathToDb)
            con.row_factory = DataBaseUtilities._json_factory
            return con
        except sqlite3.Error as error:
            UniversalUtilities.sendErrorMessageToFrontend(errorMessage=error)

    @staticmethod
    def sendDataToFrontendFromDb(sqlStatement, *sqlVariablesInOrder):
        connection = DataBaseUtilities.dbConnection()
        cursor = connection.cursor()
        cursor.execute(sqlStatement, (*sqlVariablesInOrder,))
        result = cursor.fetchall()
        connection.close()
        print(json.dumps(result))

    @staticmethod
    def insertIntoDb(sqlInsertStatement, *sqlVariablesInOrder):
        connection = DataBaseUtilities.dbConnection()
        cursor = connection.cursor()
        cursor.execute(sqlInsertStatement, (*sqlVariablesInOrder,))
        connection.commit()
        connection.close()

    @staticmethod
    def getValuesFromDb(sqlStatement, *sqlVariablesInOrder):
        connection = DataBaseUtilities.dbConnection()
        cursor = connection.cursor()
        cursor.execute(sqlStatement, (*sqlVariablesInOrder,))
        result = cursor.fetchall()
        connection.close()
        return result


class UniversalUtilities:
    @staticmethod
    def read_in_stdin_json():
        return json.loads(sys.stdin.readline())

    @staticmethod
    def sendErrorMessageToFrontend(errorMessage):
        # getting Filename and Line from which this method is called
        caller = getframeinfo(stack()[1][0])
        print(json.dumps({DictIndex.ERROR.value:  "in File {}:{}, message: {}".format(
            caller.filename, caller.lineno, str(errorMessage))}))
