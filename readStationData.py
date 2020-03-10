import handleRequest
import pymongo
import datetime

# get data from weather stations
stationDataList = []
wetterringList = ["mellau-rossstelle","damuels-jaegerstueble","damuels-hertehof","diedamskopf"]
oWetterringRequest = handleRequest.handleWetterringRequest()
now = datetime.datetime.now()
try:
    stationDataList = oWetterringRequest.getWeatherStationDataList(wetterringList)
except:
    print(now.strftime("%y.%m.%d %H:%M") + " Error: Could not read station data due to an error")
else:
    print(now.strftime("%y.%m.%d %H:%M") + " Trace: Data was received)

# write data to mongo db
mongoDbClient = pymongo.MongoClient("mongodb://localhost:27017")
dbName = "weatherData"
collectionName = "stationData"
db = mongoDbClient[dbName]
col = db[collectionName]
now = datetime.datetime.now()
try:
    col.insert_many(stationDataList)
except:
    print(now.strftime("%y.%m.%d %H:%M") + " Error: Data could not be saved to database")
else:
    print(now.strftime("%y.%m.%d %H:%M") + " Trace: Data was written to " + dbName +  " " + collectionName)




