import handleRequest
import pymongo
import datetime

# get data from weather stations
weatherDataList = []
resortsList = ["diedamskopf","mellau","damuels"]
oBergfexRequest = handleRequest.handleBergfexRequest()
now = datetime.datetime.now()
try:
    weatherDataList = oBergfexRequest.getWeatherDataList(resortsList)
except:
    print(now.strftime("%y.%m.%d %H:%M") + " Error: Could not read resort data due to an error")
else:
    print(now.strftime("%y.%m.%d %H:%M") + " Trace: Data was received")

# write data to mongo db
mongoDbClient = pymongo.MongoClient("mongodb://localhost:27017")
dbName = "weatherData"
collectionName = "prediction"
db = mongoDbClient[dbName]
col = db[collectionName]
now = datetime.datetime.now()
try:
    col.insert_many(weatherDataList)
except:
    print(now.strftime("%y.%m.%d %H:%M") + " Error: Data could not be saved to database")
else:
    print(now.strftime("%y.%m.%d %H:%M") + " Trace: Data was written to " + dbName +  " " + collectionName)



