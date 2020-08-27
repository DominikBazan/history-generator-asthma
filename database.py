import mysql.connector


def dbConnection():
    file = open("database_data.txt", "r")
    myHost = file.readline()
    myUser = file.readline()
    myPasswd = file.readline().strip()
    myDatabase = file.readline()
    file.close()

    dataBase = mysql.connector.connect(
        host = myHost,
        user = myUser,
        passwd = myPasswd,
        database = myDatabase,
        port = 11264
    )
    return dataBase
