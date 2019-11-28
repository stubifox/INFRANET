import sqlite3
import json
import getFromDb
import dataBaseConnection as dbCon


def getDefaultsFromSettingsTable():
    con = dbCon.connectDb()
    con.row_factory = getFromDb.json_factory
    dbcursor = con.cursor()
    sql = '''SELECT * FROM settings'''
    dbcursor.execute(sql)
    defSettings = dbcursor.fetchall()
    print(json.dumps(defSettings))
    con.close()


def insertDefaults(uuid, theme):
    con = dbCon.connectDb()
    dbCursor = con.cursor()
    sqlInsert = '''INSERT OR REPLACE INTO settings (key, value)
        VALUES('uuid', ?), ('theme', ?)'''
    dbCursor.execute(sqlInsert, (uuid, str(theme)))
    con.commit()
    con.close()


def main():
    try:
        inputData = dbCon.read_in_stdin()
        if inputData['load'] == 'check':
            getDefaultsFromSettingsTable()

        if inputData['load'] == 'insert':
            uuid, theme = inputData['uuid'], inputData['theme']
            insertDefaults(uuid=uuid, theme=theme)
            getDefaultsFromSettingsTable()
    except Exception as e:
        pass

    return


if __name__ == "__main__":
    main()
