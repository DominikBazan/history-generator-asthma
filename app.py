import time
from db_operations import *
from users import *
from medicines import *
from dosages import *
from userHistory import *
from allergies import *
from medicinesUsed import *
import users
import allergies
import medicines
import dosages
import medicinesUsed
import userHistory

fastRun = True
numberOfGeneratedUsers = 0 # + 'Dominik'
startTime = time.time()

if 1:
    print("Deleting all users...")
    truncateTableNamed("users")
    print("[1/6]Generating users...")
    meInsert()
    for _ in range(numberOfGeneratedUsers):
        userInsert()
    users.dbClose()
    if not fastRun:
        print("Users:")
        printTableNamed("users")

    # if 1:
    print("\nDeleting all allergies...")
    truncateTableNamed("allergies")
    print("[2/6]Generating allergies...")
    allergiesInsert()
    allergies.dbClose()
    if not fastRun:
        print("Allergies:")
        printTableNamed("allergies")
    
    # if 0:
    print("\nDeleting all medicines...")
    truncateTableNamed("medicines")
    print("[3/6]Generating medicines...")
    medicinesInsert()
    medicines.dbClose()
    if not fastRun:
        print("Medicines:")
        printTableNamed("medicines")

    # if 0:
    print("\nDeleting all dosages...")
    truncateTableNamed("dosages")
    print("[4/6]Generating dosages...")
    dosagesInsert()
    dosages.dbClose()
    if not fastRun:
        print("Dosages:")
        printTableNamed("dosages")

    # if 0:
    print("\nDeleting all medicinesUsed...")
    truncateTableNamed("medicinesUsed")
    print("[5/6]Generating medicinesUsed...")
    medicinesUsedInsert()
    medicinesUsed.dbClose()
    if not fastRun:
        print("MedicinesUsed:")
        printTableNamed("medicinesUsed")
    
# # TODO
if 1:
    print("\nRemoving the entire history of users (tables: controlTests, medicineEvents and trends) ...")
    truncateTableNamed("controlTests")
    truncateTableNamed("medicineEvents")
    # truncateTableNamed("medicinesUsed")
    truncateTableNamed("trends")
    print("[6/6]Generating users history...")
    generateUsersHistory()
    userHistory.dbClose()
    if not fastRun:
        print("Asthma triggers:")
        printTableNamed("controlTests")
        printTableNamed("medicineEvents")
        # printTableNamed("medicinesUsed")
        printTableNamed("trends")

endTime = time.time()
numberOfSeconds = endTime-startTime
numberOfCompleteMinutes = numberOfSeconds / 60
numberOfSecondsInIncompleteMinute = numberOfSeconds % 60
print("Time of execution: "+str(int(numberOfSeconds))+" s")
print("Time of execution: "+str(int(numberOfCompleteMinutes))+" min "+str(int(numberOfSecondsInIncompleteMinute))+" s")
