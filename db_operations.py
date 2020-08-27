import json
import traceback
from database import dbConnection

mysql = dbConnection()

def getAllUsers():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cur.close()
    return rows

def truncateTableNamed(tableName):
    cursor = mysql.cursor()
    cursor.execute("TRUNCATE " + tableName)
    mysql.commit()
    cursor.close()

def printTableNamed(db, tableName):
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM " + tableName)
    rows = ""
    for x in cursor:
        rows += str(x) + "\n"
    print(rows)
