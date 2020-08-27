from datetime import timedelta
from random import randrange
from tech import v2Q
import seasonsDates
from joblib import Parallel, delayed
import multiprocessing
from database import dbConnection
from csv import writer

db = dbConnection()

def generateUsersHistory():
    cursor = db.cursor(buffered=True)

    ### Zakomentować dwie poniższe linijki jeśli nie chcę czyścić wcześniejszych wyników
    
    # open("CSV1.csv", 'w').close()
    # open("CSV2.csv", 'w').close()
    
    ### Zakomentować trzy poniższe linijki jeśli nie chcę czyścić wcześniejszych wyników
    
    # header = ['id_user', 'date', 'avr14', 'avr5', 'W-1', 'negative_med_change', 'positive_med_change', 'max_dusting', 'rain', 'wind', 'temperature', 'W0', 'W0-avr14']
    # appendLineToFile(header, "CSV1.csv")
    # appendLineToFile(header, "CSV2.csv")

    # wormup date
    wormupDate = seasonsDates.wormupDate
    # start of 1st CSV
    winterStartDate2017 = seasonsDates.winterStartDate2017
    # start of 2nd CSV
    winterStartDate2018 = seasonsDates.winterStartDate
    # finish date
    winter2StartDate = seasonsDates.winter2StartDate

    allWeather, allWeatherValues = getAllWeather()

    cursor.execute("SELECT count(*) FROM users")
    res = cursor.fetchone()
    numberOfUsers = res[0]

    # cursor.execute("SELECT u.id_user AS id_user, ct.id_control_test FROM users u LEFT JOIN controlTests ct ON (u.id_user=ct.id_user) WHERE ct.id_control_test IS NULL")
    cursor.execute("SELECT id_user FROM users u")
    
    users = [id_user[0] for id_user in cursor]

    for i in range(1,seasonsDates.N+1):
        users.remove(i)

    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(processInputUsers)(id_user, wormupDate, winterStartDate2017, winterStartDate2018, winter2StartDate, numberOfUsers, allWeather, allWeatherValues) for id_user in users)

    cursor.close()


def processInputUsers(idUser, wormupDate, winterStartDate2017, winterStartDate2018, winter2StartDate, numberOfUsers, allWeather, allWeatherValues):
    db = dbConnection()

    today = wormupDate

    thisUsersAllergiesNames = getThisUsersAllergiesNames(idUser)

    last14AsthmaResultsAfterDailyMedicinesQueue = []
    last14AsthmaResultsQueue = []
    dosagesFrom5DaysBackQueue = []
    dosagesIdsFrom5DaysBackQueue = []
    dosageChangeQueue = []
    dosageChangeLogQueue = []
    dosageIncreaseCounter = 0
    dosageDecreaseCounter = 0

    # controlTestList = []
    # medicineEventsList = []
    # trendsList = []

    # For each day in a time slot
    while today < winter2StartDate:
        # LOG
        # print(str(last14AsthmaResultsAfterDailyMedicinesQueue) + " last14AsthmaResultsAfterDailyMedicinesQueue")
        #print(str(dosagesFrom5DaysBackQueue) + " dosagesFrom5DaysBackQueue")
        # print(str(dosagesIdsFrom5DaysBackQueue) + " dosagesIdsFrom5DaysBackQueue")
        # print(str(dosageChangeQueue) + " dosageChangeQueue")

        todayStr = today.strftime("%Y-%m-%d")

        # progress bar
        # comment this for maximum speed
        v = int((today - wormupDate).days / 750 * 100)
        string = ""
        for _ in range(v): string += "#"
        for _ in range(100-v): string += " "
        print(str(idUser) + " [" + string + "]")

        if today == winterStartDate2017:
            fileName = 'CSV1.csv'
        elif today == winterStartDate2018:
            fileName = 'CSV2.csv'

        dailyDataLine = [idUser, todayStr, "", "", "", "", "", "", allWeatherValues[todayStr][0], allWeatherValues[todayStr][1], allWeatherValues[todayStr][2], "", ""]
        
        # counting number of both types of changes in dosageChangeLogQueue
        positiveChange = 0
        negativeChange = 0
        for change in dosageChangeLogQueue:
            if change[:1] == "+":
                positiveChange += 1
            elif change == "0":
                pass
            else:
                negativeChange += 1
        dailyDataLine[5] = negativeChange
        dailyDataLine[6] = positiveChange
        
        # Condidions log
        # logTable = [idUser]  # LOG
        W = 25
        numberOfFactorsUsedForRandomizationOfWMedicinesChange = 0

        # DONE 1. pylenie
        ifIsAnyDusting = False
        maxTodaysDustingPoints = 0
        for allerieName in thisUsersAllergiesNames:
            todaysDustingPoints = getTodaysDustingPointsForName(getSeason36(today), allerieName)
            if todaysDustingPoints != 0:
                ifIsAnyDusting = True
            if maxTodaysDustingPoints < todaysDustingPoints:
                maxTodaysDustingPoints = todaysDustingPoints
        W -= maxTodaysDustingPoints
        dailyDataLine[7] = maxTodaysDustingPoints
        # logTable.append(maxTodaysDustingPoints) # LOG
        
        # DONE 2. deszcz
        if ifIsAnyDusting and allWeather[todayStr][0]:
            # logTable.append("R")  # LOG
            W += 1
        else:
            # logTable.append(" ")  # LOG
            pass
            
        # DONE 3. wiatr
        if ifIsAnyDusting and allWeather[todayStr][1]:
            # logTable.append("W")  # LOG
            numberOfFactorsUsedForRandomizationOfWMedicinesChange += 1
            W -= 1
        else:
            # logTable.append(" ")  # LOG
            pass
        
        # DONE 4. temperatura
        if ifIsAnyDusting and allWeather[todayStr][2]:
            # logTable.append("T")  # LOG
            numberOfFactorsUsedForRandomizationOfWMedicinesChange += 1
            W -= 1
        else:
            # logTable.append(" ")  # LOG
            pass
        
        # 5. zmiany dawek leków
        if dosageIncreaseCounter >= 2:
            # replaceing "+N"s with "0" in queue, subtraction from counter 2 and change of W
            for index in range(len(dosageChangeQueue)):
                if dosageChangeQueue[index][:1] == "+":
                    dosageChangeQueue[index] = "0"
            dosageIncreaseCounter -= 2
            W -= 2
            # logTable.append("W-2")  # LOG
        elif dosageDecreaseCounter >= 2:
            # replaceing "-N"s with "0" in queue, adding to counter 2 and change of W
            for index in range(len(dosageChangeQueue)):
                if dosageChangeQueue[index][:1] == "-":
                    dosageChangeQueue[index] = "0"
            dosageDecreaseCounter -= 2
            W += 2
            # logTable.append("W+2")  # LOG
        else:
            # logTable.append("W+0")  # LOG
            pass

        # DONE 6. zmiana tendencji
        arithmeticAverage = 0
        lenList = len(last14AsthmaResultsAfterDailyMedicinesQueue)
        if lenList >= 5:
            arithmeticAverage = countArithmeticAverage(last14AsthmaResultsAfterDailyMedicinesQueue)
            numberOfElementsGraterThanArithmeticAverage = 0
            for index in range(lenList-5, lenList):
                if last14AsthmaResultsAfterDailyMedicinesQueue[index] > arithmeticAverage:
                    numberOfElementsGraterThanArithmeticAverage += 1 
            if numberOfElementsGraterThanArithmeticAverage >= 3:
                # # UWAGA Zmieniłem 2 na 1!
                W += 2
                # logTable.append("+")
            else:
                # # UWAGA Zmieniłem 2 na 1!
                W -= 2
                # logTable.append("-")
        else:
            # logTable.append("0")
            pass
        
        ### Sprawdzam czy wystąpi ZMIANA LEKU i go zmieniam oraz obliczam WMedicines (W')
        if len(dosagesIdsFrom5DaysBackQueue) > 0:
            lastDosageId = dosagesIdsFrom5DaysBackQueue[len(dosagesIdsFrom5DaysBackQueue)-1]
            lastDosageValue = dosagesFrom5DaysBackQueue[len(dosagesFrom5DaysBackQueue)-1]
        else:
            lastDosageId = 1
            lastDosageValue = "0"
        
        # INFO: not changing dosage between x and y
        x = 25
        y = 21
        if W > x:
            numberOfDosagesNeeded = -int((W - 25)/2)
        elif W < y:
            numberOfDosagesNeeded = int((25 - W)/2)
        else:
            numberOfDosagesNeeded = 0

        numberOfDosagesToIncrease = numberOfDosagesNeeded - int(lastDosageValue)

        # LOG
        # if numberOfDosagesToIncrease > 0 and lastDosageValue == "10":
        #     print("Nie można ZWIĘKSZYĆ dawki!")
        # elif (numberOfDosagesToIncrease < 0 and lastDosageValue == "0"):
        #     print("Nie można ZMNIEJSZYĆ dawki!")

        # I assume the patient is taking their medication every day
        if numberOfDosagesToIncrease > 0 and lastDosageValue != "10":
            # increase
            maxIncreasePossible = 10 - int(lastDosageValue)
            if maxIncreasePossible < numberOfDosagesToIncrease:
                numberOfDosagesToIncrease = maxIncreasePossible
            dosageChangeQueue.append("+"+str(numberOfDosagesToIncrease))
            if len(dosageChangeQueue) > 5:
                dosageChangeQueue.pop(0)
            dosageChangeLogQueue.append("+"+str(numberOfDosagesToIncrease))
            if len(dosageChangeLogQueue) > 5:
                dosageChangeLogQueue.pop(0)

            dosageIncreaseCounter += 1
            # TODO ARCHIWIZACJA
            # medicineEventsList.append((idUser, 1, todayStr, lastDosageId+numberOfDosagesToIncrease,))
            dosagesFrom5DaysBackQueue.append(str(int(lastDosageValue)+numberOfDosagesToIncrease))
            if len(dosagesFrom5DaysBackQueue) > 5:
                dosagesFrom5DaysBackQueue.pop(0)
            dosagesIdsFrom5DaysBackQueue.append(lastDosageId+numberOfDosagesToIncrease)
            if len(dosagesIdsFrom5DaysBackQueue) > 5:
                dosagesIdsFrom5DaysBackQueue.pop(0)
            
            WMedicines = W
            if ifIsAnyDusting:
                for _ in range(numberOfDosagesNeeded):
                    if numberOfFactorsUsedForRandomizationOfWMedicinesChange == 0:
                        # chance = 95
                        chance = 90
                    if numberOfFactorsUsedForRandomizationOfWMedicinesChange == 1:
                        # chance = 80
                        chance = 85
                    else:
                        # INFO: numberOfFactorsUsedForRandomizationOfWMedicinesChange == 2:
                        # chance = 60
                        chance = 55
                    if randrange(101) <= chance:
                        WMedicines += 2
                    else:
                        pass
        elif numberOfDosagesToIncrease < 0 and lastDosageValue != "0":
            # decrease
            numberOfDosagesToDecrease = -numberOfDosagesToIncrease
            maxDecreasePossible = 0 + int(lastDosageValue)
            if maxDecreasePossible < numberOfDosagesToDecrease:
                numberOfDosagesToDecrease = numberOfDosagesToDecrease
            dosageChangeQueue.append("-"+str(numberOfDosagesToDecrease))
            if len(dosageChangeQueue) > 5:
                dosageChangeQueue.pop(0)
            dosageChangeLogQueue.append("-"+str(numberOfDosagesToDecrease))
            if len(dosageChangeLogQueue) > 5:
                dosageChangeLogQueue.pop(0)    
            dosageDecreaseCounter += 1
            # TODO ARCHIWIZACJA
            # medicineEventsList.append((idUser, 1, todayStr, lastDosageId-numberOfDosagesToDecrease,))
            dosagesFrom5DaysBackQueue.append(str(int(lastDosageValue)-numberOfDosagesToDecrease))
            if len(dosagesFrom5DaysBackQueue) > 5:
                dosagesFrom5DaysBackQueue.pop(0)
            dosagesIdsFrom5DaysBackQueue.append(lastDosageId-numberOfDosagesToDecrease)
            if len(dosagesIdsFrom5DaysBackQueue) > 5:
                dosagesIdsFrom5DaysBackQueue.pop(0)
            WMedicines = W
        else:
            # nie zmieniac
            # too low dose OR too high dose OR stable situation
            dosageChangeQueue.append("0")
            if len(dosageChangeQueue) > 5:
                dosageChangeQueue.pop(0)
            dosageChangeLogQueue.append("0")
            if len(dosageChangeLogQueue) > 5:
                dosageChangeLogQueue.pop(0)
            # TODO ARCHIWIZACJA
            # medicineEventsList.append((idUser, 1, todayStr, lastDosageId,))
            dosagesFrom5DaysBackQueue.append(lastDosageValue)
            if len(dosagesFrom5DaysBackQueue) > 5:
                dosagesFrom5DaysBackQueue.pop(0)
            dosagesIdsFrom5DaysBackQueue.append(lastDosageId)
            if len(dosagesIdsFrom5DaysBackQueue) > 5:
                dosagesIdsFrom5DaysBackQueue.pop(0)
            WMedicines = W

        # LOG
        # if len(dosagesFrom5DaysBackQueue) != 0:
        #     logTable.append(dosagesFrom5DaysBackQueue[len(dosagesFrom5DaysBackQueue)-1])

        # Saving W and WMedicines to database
        if W > 25:
            W = 25
        if W < 5:
            W = 5 
        if WMedicines > 25:
            WMedicines = 25
        if WMedicines < 5:
            WMedicines = 5
        # TODO ARCHIWIZACJA 
        # controlTestList.append((idUser, todayStr, W, WMedicines,))

        # adding avr W14
        dailyDataLine[2] = countArithmeticAverage(last14AsthmaResultsQueue)
        # adding avr W5
        dailyDataLine[3] = countArithmeticAverage(last14AsthmaResultsQueue[-5:])
        # adding W to last14AsthmaResultsQueue
        last14AsthmaResultsQueue.append(W)
        if len(last14AsthmaResultsQueue) > 14:
                last14AsthmaResultsQueue.pop(0)
        # adding W-1
        dailyDataLine[4] = last14AsthmaResultsQueue[-1]
        # adding W0
        dailyDataLine[11] = W
        # adding W0-avr W14
        dailyDataLine[12] = dailyDataLine[2] - W

        last14AsthmaResultsAfterDailyMedicinesQueue.append(WMedicines)
        if len(last14AsthmaResultsAfterDailyMedicinesQueue) > 14:
            last14AsthmaResultsAfterDailyMedicinesQueue.pop(0)

        # LOG
        # if W < 16:
        #     print("W poniżej 16!")
        # if WMedicines < 16:
        #     print("WMedicines poniżej 16!")

        # Calculation of the trend
        if arithmeticAverage == 0:
            trend = "0"
        else:
            if WMedicines < arithmeticAverage - 1:
                if WMedicines == 5:
                    trend = "0" 
                else:
                    trend = "-1"
            elif WMedicines > arithmeticAverage + 1:
                if WMedicines == 25:
                    trend = "0"
                else:
                    trend = "+1"
            else:
                trend = "0"
        # TODO ARCHIWIZACJA ?
        # trendsList.append((idUser, todayStr, trend,))
    
        # logTable.append(trend)
    

        # print(dailyDataLine)
        if today >= winterStartDate2017:
            appendLineToFile(dailyDataLine, fileName)

        # print("U: %s  Data: %s  W:[%s,%s]  Pylenie:%s Deszcz:%s Wiatr:%s Temp.:%s Zm. dawki: %s Zm.tend.: %s  Dosage: %s Trend: %s" % (logTable[0], todayStr, W, WMedicines, logTable[1], logTable[2], logTable[3], logTable[4], logTable[5], logTable[6], logTable[7], logTable[8]))   # LOG

        today += timedelta(days=1)

    # print("Saving history to database... " + str(idUser))
    # TODO ARCHIWIZACJA
    # dbSave(controlTestList, medicineEventsList, trendsList)

    db.close()

########################################################################
########################################################################
########################################################################

def getThisUsersAllergiesNames(idUser):
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT name FROM allergies WHERE id_user=%s", (idUser,))
    thisUsersAllergiesNames = [nameRow[0] for nameRow in cursor]
    cursor.close()
    return thisUsersAllergiesNames

def getAllWeather():
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT date, rain, wind, temperature FROM weather")
    allWeather = {}
    allWeatherValues = {}
    for weatherRow in cursor:
        if int(weatherRow[1]) > 5:
            rain = True
        else:
            rain = False
        if int(weatherRow[2]) > 4.5:
            wind = True
        else:
            wind = False
        if int(weatherRow[3]) > 25:
            temperature = True
        else:
            temperature = False
        allWeatherValues[weatherRow[0].strftime("%Y-%m-%d")] = (weatherRow[1], weatherRow[2], weatherRow[3],)
        allWeather[weatherRow[0].strftime("%Y-%m-%d")] = (rain, wind, temperature,)
    cursor.close()
    return allWeather, allWeatherValues

def getTodaysDustingPointsForName(season36, allerieName):
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT " + season36 + " FROM asthmaFactors WHERE name=%s", (allerieName,))
    dustingPointRow = cursor.fetchone()
    todaysDustingPointsForName = dustingPointRow[0]
    cursor.close()
    return todaysDustingPointsForName

def getSeason36(today):
    day = today.day
    month = today.month
    
    if day > 20:
        partOfMonth123 = "3"
    elif day > 10:
        partOfMonth123 = "2"
    else:
        partOfMonth123 = "1"
    
    monthNames = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

    return monthNames[month-1] + partOfMonth123
    
def findDosageChanges(dosagesFrom5DaysBack):
    increasesCounter = 0
    reductionCounter = 0
    for i in range(len(dosagesFrom5DaysBack)):
        if i == 0: continue
        delta = int(dosagesFrom5DaysBack[i-1]) - int(dosagesFrom5DaysBack[i])
        if delta > 0:
            reductionCounter += 1
        if delta < 0:
            increasesCounter += 1
    return increasesCounter, reductionCounter
    
def countArithmeticAverage(list):
    listLen = len(list)
    if listLen == 0:
        return 0
    sum = 0
    for element in list:
        sum = sum + element
    return sum / len(list)

# def dbSave(controlTestsList, medicineEventsList, trendsList):
#     cursor = db.cursor()
#     for controlTest in controlTestsList:
#         cursor.execute("INSERT INTO controlTests (id_user, date, value, value_medicines) VALUES (%s, %s, %s, %s)", (controlTest[0], controlTest[1], controlTest[2], controlTest[3],))
#     for medicineEvents in medicineEventsList:
#         cursor.execute("INSERT INTO medicineEvents (id_user, implemented, date, id_dosage) VALUES (%s, %s, %s, %s)", (medicineEvents[0], medicineEvents[1], medicineEvents[2], medicineEvents[3],))
#     for trend in trendsList:
#         cursor.execute("INSERT INTO trends (id_user, date, trend) VALUES (%s, %s, %s)", (trend[0], trend[1], trend[2],))
#     db.commit()
#     cursor.close()

def appendLineToFile(line, file_name):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(line)

def dbClose():
    db.close()
  