import handleRequest
import handleMongoDb
import datetime

# get weather dict
# resortsList = ["diedamskopf","mellau"]
# oBergfexRequest = handleRequest.handleBergfexRequest()
# weatherDataDict = oBergfexRequest.getWeatherDataList(resortsList)

# # insert in db
# now = datetime.datetime.now()
# handleMongoDb.insertDict(weatherDataDict,"weatherData", "date_" + now.strftime("%d_%m_%Y"))

wetterringList = ["mellau-rossstelle"]
oWetterringRequest = handleRequest.handleWetterringRequest()
stationData = oWetterringRequest.getWeatherStationDataList(wetterringList)
