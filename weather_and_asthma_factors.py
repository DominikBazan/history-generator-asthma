from database import dbConnection

db = dbConnection()

def weatherAndAsthmaFactorsInsert():
    weatherFilePath1 = "./weather_history_17_18.txt"
    weatherFilePath2 = "./weather_history_18_19.txt"

    for weatherFilePath in [weatherFilePath1, weatherFilePath2]:
        cursor = db.cursor()
        f = open(weatherFilePath, "r")
        header = f.readline()
        for line in f: 
            record = line.split()
            query = 'INSERT INTO weather (date, temperature, humidity, wind, rain)\
                VALUES ("{0}", {1}, {2}, {3}, {4});'.format(record[0], record[2], record[5], record[8], record[13])
            # print(query)
            cursor.execute(query)
        db.commit()
        print("Weather is loaded")
        cursor.close()


    asthmaFactorsFilePath = "./asthma_factors_history.txt"
    cursor = db.cursor()
    f = open(asthmaFactorsFilePath, "r")
    for l in f: 
        line = l.split()
        data = '\"' + line[0] + '\"'
        for el in range(1,len(line)):
            data += ("," + line[el])
        query = 'INSERT INTO asthmaFactors VALUES (' + data + ');'
        # print(query)
        cursor.execute(query)
    db.commit()
    print("Asthma factors is loaded")
    cursor.close()
