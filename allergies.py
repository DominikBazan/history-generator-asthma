from random import randrange
from tech import v2Q
from database import *
import multiprocessing
from joblib import Parallel, delayed
import seasonsDates

db = dbConnection()

def allergiesInsert():
    cursor = db.cursor()

    cursor.execute("SELECT name FROM asthmaFactors")
    listAllegiesNames = [name[0] for name in cursor]


    # cursor.execute("SELECT u.id_user AS id_user, ct.id_control_test FROM users u LEFT JOIN controlTests ct ON (u.id_user=ct.id_user) WHERE ct.id_control_test IS NULL")
    cursor.execute("SELECT id_user FROM users")
    users = [user[0] for user in cursor]
    
    for i in range(1,seasonsDates.N+1):
        users.remove(i)

    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(addUsersAllergies)(userId, listAllegiesNames) for userId in users)
    
    cursor.close()

def addUsersAllergies(idUser, listAllegiesNames):
    # adding allergies for one user
    numberOfAlergies = randrange(4) + 1

    # TODO fixed on 4
    numberOfAlergies = 4

    randomAlergiesNames = []
    for _ in range(numberOfAlergies):
        index = randrange(len(listAllegiesNames))
        randomAlergiesNames.append(listAllegiesNames[index])
        listAllegiesNames.pop(index)
    cursor = db.cursor()
    for name in randomAlergiesNames:
        cursor.execute("INSERT INTO allergies (id_user, name) VALUES (%s, %s)", (idUser, name,))
    db.commit()

def dbClose():
    db.close()
