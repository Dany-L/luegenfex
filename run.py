import handleRequest
import handleMongoDb
import datetime

# get weather dict
resortsList = ["diedamskopf","mellau"]
oHandleRequest = handleRequest.handleBergfexRequest()
weatherDataDict = oHandleRequest.getWeatherDataList(resortsList)

# insert in db
now = datetime.datetime.now()
handleMongoDb.insertDict(weatherDataDict,"weatherData", "date_" + now.strftime("%d_%m_%Y"))
