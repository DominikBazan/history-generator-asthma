from tech import v2Q
from database import *

db = dbConnection()

def medicinesInsert():
    cursor = db.cursor()

    medicines = ["SYMBICORT", "BUFOMIX EASYHALER", "SALMEX DYSK", "ASARIS DYSK", "SINGULAIR", "MONTELUKAST", "MONKASTA", "EUPMYLLIN", "THEOSPIREX"]

    medicinesToAdd = ""

    medicinesLength = len(medicines)
    for medicineIndex in range(medicinesLength):
        medicinesToAdd += ("(" + v2Q(medicines[medicineIndex]) + ")")
        if medicineIndex < medicinesLength - 1:
            medicinesToAdd += ", "

    query = "INSERT INTO medicines (name) VALUES " + medicinesToAdd

    cursor.execute(query)
    db.commit()
    cursor.close()

def dbClose():
    db.close()
