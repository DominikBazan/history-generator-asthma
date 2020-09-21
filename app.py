import time
from db_operations import *
from weather_and_asthma_factors import *
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
numberOfGeneratedUsers = 4 # if set: +='Dominik' as 1
startTime = time.time()

# If I want to switch to append and not overwrite mode then I have to:
#> Comment out two lines to delete the content of CSV files.
#> Comment out 3 lines adding headers.
#> Comment on clearing arrays.
#> Set the number of users already generated in the seassonDates.py file.

if 1:
    print("Deleting all weather and asthma factors...")
    truncateTableNamed("weather")
    truncateTableNamed("asthmaFactors")
    print("[1/7]Generating weather and asthma factors...")
    weatherAndAsthmaFactorsInsert()

if 1:
    print("Deleting all users...")
    truncateTableNamed("users")
    print("[2/7]Generating users...")
    # meInsert()
    for _ in range(numberOfGeneratedUsers):
        userInsert()
    users.dbClose()
    if not fastRun:
        print("Users:")
        printTableNamed("users")

    # if 1:
    print("\nDeleting all allergies...")
    truncateTableNamed("allergies")
    print("[3/7]Generating allergies...")
    allergiesInsert()
    allergies.dbClose()
    if not fastRun:
        print("Allergies:")
        printTableNamed("allergies")

    # if 0:
    print("\nDeleting all medicinesUsed...")
    truncateTableNamed("medicinesUsed")
    print("[4/7]Generating medicinesUsed...")
    medicinesUsedInsert()
    medicinesUsed.dbClose()
    if not fastRun:
        print("MedicinesUsed:")
        printTableNamed("medicinesUsed")
    
# If I do this, I have to do medicinesUsed as well
if 1:
    print("\nDeleting all medicines...")
    truncateTableNamed("medicines")
    print("[5/7]Generating medicines...")
    medicinesInsert()
    medicines.dbClose()
    if not fastRun:
        print("Medicines:")
        printTableNamed("medicines")

if 1:
    print("\nDeleting all dosages...")
    truncateTableNamed("dosages")
    print("[6/7]Generating dosages...")
    dosagesInsert()
    dosages.dbClose()
    if not fastRun:
        print("Dosages:")
        printTableNamed("dosages")
    
if 1:
    print("\nRemoving the entire history of users (tables: controlTests, medicineEvents and trends) ...")
    truncateTableNamed("controlTests")
    truncateTableNamed("medicineEvents")
    truncateTableNamed("trends")
    print("[7/7]Generating users history...")
    generateUsersHistory()
    # userHistory.dbClose()
    if not fastRun:
        print("Asthma triggers:")
        printTableNamed("controlTests")
        printTableNamed("medicineEvents")
        printTableNamed("trends")

endTime = time.time()
numberOfSeconds = endTime-startTime
numberOfCompleteMinutes = numberOfSeconds / 60
numberOfSecondsInIncompleteMinute = numberOfSeconds % 60
print("Time of execution: "+str(int(numberOfSeconds))+" s")
print("Time of execution: "+str(int(numberOfCompleteMinutes))+" min "+str(int(numberOfSecondsInIncompleteMinute))+" s")
