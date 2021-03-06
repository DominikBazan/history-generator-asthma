from random import randrange
from tech import v2Q
from database import *
import multiprocessing
from joblib import Parallel, delayed
from seasonsDates import *
import seasonsDates

db = dbConnection()

def medicinesUsedInsert():
    cursor = db.cursor()
    # cursor.execute("SELECT u.id_user AS id_user, ct.id_control_test FROM users u LEFT JOIN controlTests ct ON (u.id_user=ct.id_user) WHERE ct.id_control_test IS NULL")
    cursor.execute("SELECT id_user FROM users")
    users = [user[0] for user in cursor]
    
    for i in range(1,seasonsDates.N+1):
        users.remove(i)
    
    medicinesIds = getMedicinesIds()

    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(addUsersMedicinesUsed)(userId, medicinesIds) for userId in users)
    
    cursor.close()

def getMedicinesIds():
    cursor = db.cursor()
    cursor.execute("SELECT id_medicine FROM medicines")
    result = [medicineRow[0] for medicineRow in cursor]
    cursor.close()
    return result

def addUsersMedicinesUsed(userId, medicinesIds):
    randomMedicineId = medicinesIds[randrange(len(medicinesIds))]
    cursor = db.cursor()
    cursor.execute("INSERT INTO medicinesUsed (id_medicine, id_user, start_date, stop_date) VALUES (%s, %s, %s, %s)", (randomMedicineId, userId, seasonsDates.winterStartDate, seasonsDates.winter2StartDate,))
    db.commit()
    cursor.close()

def dbClose():
    db.close()
