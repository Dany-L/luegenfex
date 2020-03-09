import handleRequest
import pymongo
import datetime

fId = open("request.log","a")

# get data from weather stations
stationDataList = []
wetterringList = ["mellau-rossstelle","damuels-jaegerstueble","damuels-hertehof","diedamskopf"]
oWetterringRequest = handleRequest.handleWetterringRequest()
now = datetime.datetime.now()
try:
    stationDataList = oWetterringRequest.getWeatherStationDataList(wetterringList)
except:
    fId.write(now.strftime("%y.%m.%d %H:%M") + " Error: Could not read station data due to an error\n")
else:
    fId.write(now.strftime("%y.%m.%d %H:%M") + " Trace: Data was received \n")

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
    fId.write(now.strftime("%y.%m.%d %H:%M") + " Error: Data could not be saved to database \n")
else:
    fId.write(now.strftime("%y.%m.%d %H:%M") + " Trace: Data was written to " + dbName +  " " + collectionName + "\n")
fId.close()



