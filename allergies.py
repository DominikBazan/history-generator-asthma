from random import randrange
from tech import v2Q
from database import *
import multiprocessing
from joblib import Parallel, delayed
import seasonsDates

db = dbConnection()

allergiesToInsert = []

def allergiesInsert():
    cursor = db.cursor()

    cursor.execute("SELECT name FROM asthmaFactors")
    listAllegiesNames = [name[0] for name in cursor]

    # cursor.execute("SELECT u.id_user AS id_user, ct.id_control_test FROM users u LEFT JOIN controlTests ct ON (u.id_user=ct.id_user) WHERE ct.id_control_test IS NULL")
    cursor.execute("SELECT id_user FROM users")
    users = [user[0] for user in cursor]
    
    for i in range(1,seasonsDates.N+1):
        users.remove(i)

    for userId in users:
        addUsersAllergies(userId, listAllegiesNames) 
    
    cursor.close()

def addUsersAllergies(idUser, listAllegiesNames):
    # adding allergies for one user
    numberOfAlergies = randrange(4) + 1

    listAllegiesNamesCopy = [el for el in listAllegiesNames]

    # TODO fixed on 4
    numberOfAlergies = 4

    randomAlergiesNames = []
    for _ in range(numberOfAlergies):
        index = randrange(len(listAllegiesNamesCopy))
        randomAlergiesNames.append(listAllegiesNamesCopy[index])
        listAllegiesNamesCopy.pop(index)
    
    for name in randomAlergiesNames:
        allergiesToInsert.append((idUser, name,))
    
def dbClose():
    print("Adding generated allergies to database...")
    cursor = db.cursor()

    rowsStr = ""
    for allergie in allergiesToInsert:
        rowsStr += "(" + str(allergie[0]) + "," + v2Q(allergie[1]) + "),"
        
    cursor.execute("INSERT INTO allergies (id_user, name) VALUES " + rowsStr[:-1])

    db.commit()
    cursor.close()

    db.close()
