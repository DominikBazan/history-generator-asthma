import base64
from faker import Faker
from random import randrange
from datetime import timedelta
from tech import v2Q
from tech import datetimeToStr
from database import *

db = dbConnection()

usersToInsert = []

def userInsert():
    # cursor = db.cursor()

    fake = Faker(['pl_PL'])

    # preparing random data
    while True:
        nameAndSurname = fake.name()
        name = nameAndSurname.split()[0]
        surname = nameAndSurname.split()[1]
        if name != "pan" and name != "pani":
            break

    if randrange(2) == 0:
        sex = "M"
    else:
        sex = "F"

    email = fake.safe_email()

    dateOfBirth = fake.date_of_birth(tzinfo=None, minimum_age=15, maximum_age=50)

    birth = datetimeToStr(dateOfBirth)

    if sex == "M":
        height = randrange(40) + 155
    else:
        height = randrange(37) + 145

    if sex == "M":
        weight = randrange(30) + 60
    else:
        weight = randrange(30) + 45

    daysTillDisease = 10*365 + randrange(40*365)    # 50 - is the oldest possible illness start
    disease_start = datetimeToStr(dateOfBirth + timedelta(days=daysTillDisease))

    password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

    type = randrange(2)

    usersToInsert.append((name, surname, sex, email, birth, height, weight, disease_start, type,)) # pollen_asthma, 

    # # inserting random data
    # queryTemplate = "INSERT INTO users (name, surname, sex, email, birth, height, weight, disease_start, password, pollen_asthma, type) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, \"{}\", {}, {})"
    # insertQuery = queryTemplate.format(v2Q(name), v2Q(surname), v2Q(sex), v2Q(email), v2Q(birth), height, weight, v2Q(disease_start), "$2a$12$VDzKDo.tKswYjFi6HW3VHuINAKNTVq4bv9PBz2MgvCwCvFu8.PfH2", type)
    # cursor.execute(insertQuery)

    # db.commit()
    # cursor.close()

def meInsert():
    cursor = db.cursor()
    queryTemplate = "INSERT INTO users (name, surname, sex, email, birth, height, weight, disease_start, password, pollen_asthma) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, \"{}\", {})"
    insertQuery = queryTemplate.format(v2Q("Dominik"), v2Q("Bazan"), v2Q('M'), v2Q("dominik@gmail.com"), v2Q("1996-04-23"), 173, 70, v2Q('2010-10-10'), "$2a$12$VDzKDo.tKswYjFi6HW3VHuINAKNTVq4bv9PBz2MgvCwCvFu8.PfH2", "TRUE")
    # insertQuery = queryTemplate.format(v2Q("Dominik"), v2Q("Bazan"), v2Q('M'), v2Q("dominik@gmail.com"), v2Q("1996-04-23"), 173, 70, v2Q('2010-10-10'), base64.b64encode('password'.encode("utf-8")))
    cursor.execute(insertQuery)
    db.commit()
    cursor.close()

def dbClose():
    print("Adding generated users to database...")
    cursor = db.cursor()
    
    rowsStr = ""
    for user in usersToInsert:
        # inserting random data
        
        # queryTemplate = "INSERT INTO users (name, surname, sex, email, birth, height, weight, disease_start, password, pollen_asthma, type) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, \"{}\", {}, {})"
        # insertQuery = queryTemplate.format(v2Q(user[0]), v2Q(user[1]), v2Q(user[2]), v2Q(user[3]), v2Q(user[4]), user[5], user[6], v2Q(user[7]), "$2a$12$VDzKDo.tKswYjFi6HW3VHuINAKNTVq4bv9PBz2MgvCwCvFu8.PfH2", user[8], user[9])
        # cursor.execute(insertQuery)

        rowsStr += "(" + v2Q(user[0]) + "," + v2Q(user[1]) + "," + v2Q(user[2]) + "," + v2Q(user[3]) + "," + v2Q(user[4]) + "," + str(user[5]) + "," + str(user[6]) + "," + v2Q(user[7]) + ",\"" + "$2a$12$VDzKDo.tKswYjFi6HW3VHuINAKNTVq4bv9PBz2MgvCwCvFu8.PfH2" + "\"," + str(user[8]) + "),"

    # cursor.execute("INSERT INTO users (name, surname, sex, email, birth, height, weight, disease_start, password, pollen_asthma, type) VALUES " + rowsStr[:-1])
    cursor.execute("INSERT INTO users (name, surname, sex, email, birth, height, weight, disease_start, password, type) VALUES " + rowsStr[:-1])

    db.commit()
    cursor.close()

    db.close()
