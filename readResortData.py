import handleRequest
import pymongo
import datetime

fId = open("request.log","a")

# get data from weather stations
weatherDataList = []
resortsList = ["diedamskopf","mellau","damuels"]
oBergfexRequest = handleRequest.handleBergfexRequest()
now = datetime.datetime.now()
try:
    weatherDataList = oBergfexRequest.getWeatherDataList(resortsList)
except:
    fId.write(now.strftime("%y.%m.%d %H:%M") + " Error: Could not read resort data due to an error\n")
else:
    fId.write(now.strftime("%y.%m.%d %H:%M") + " Trace: Data was received \n")

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
    fId.write(now.strftime("%y.%m.%d %H:%M") + " Error: Data could not be saved to database \n")
else:
    fId.write(now.strftime("%y.%m.%d %H:%M") + " Trace: Data was written to " + dbName +  " " + collectionName + "\n")
fId.close()



