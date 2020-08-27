from tech import v2Q
from database import *

db = dbConnection()

def dosagesInsert():
    cursor = db.cursor()

    dosages = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    dosagesToAdd = ""

    dosagesLength = len(dosages)
    for dosageIndex in range(dosagesLength):
        dosagesToAdd += ("(" + v2Q(dosages[dosageIndex]) + ")")
        if dosageIndex < dosagesLength - 1:
            dosagesToAdd += ", "

    query = "INSERT INTO dosages (dosage) VALUES " + dosagesToAdd

    cursor.execute(query)
    db.commit()
    cursor.close()

def dbClose():
    db.close()
