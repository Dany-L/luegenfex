import requests
# from html.parser import HTMLParser
from bs4 import BeautifulSoup
import datetime
import re
import json


class handleRequest:

    def __init__(self,resortList,rootUrl,postFixUrl):
        self.resortList = resortList
        self.rootUrl = rootUrl
        self.postFixUrl = postFixUrl

    def getWeatherDataList(self):
        weatherDataDict = dict()
        # iterate over all resorts
        for resort in self.resortList:
            resortInfoDict = self.getWeatherData(resort)
            weatherDataDict[resort] = resortInfoDict

        # return weather dict
        return weatherDataDict

    def getWeatherData(self,resort):

        resortUrl = self.rootUrl + resort + self.postFixUrl
        request = requests.get(url = resortUrl)
        resortSoup = BeautifulSoup(request.text, 'html.parser')

        # now
        date = datetime.datetime.now()

        # initialize weather dict
        weatherDict = dict()

        for day in range(9):
            
            # date of day
            dateDay = date + datetime.timedelta(days=day)
            
            idStr = "forecast-day-" + str(day)
            forecastDayRaw = resortSoup.find("div", id=idStr)
            forecastDayRawSoup = BeautifulSoup(str(forecastDayRaw), 'html.parser')

            dataDict = {
                "mountain": ["tmax","tmin","nschnee"],
                "valley": ["tmax","tmin","nschnee"],
                "rainProb": ["rrp"],
                "rainAmountSun": ["rrr","sonne"],
                "snowLine": [],
                "storm": ["wgew"],
                "wind": ["ff"]
            }

            groupRawList = forecastDayRawSoup.find_all("div",class_="group")
            groupIdx = 0

            # init weather day dictionary
            detailsDict = dict()

            for dataName in dataDict:

                groupSoup = BeautifulSoup(str(groupRawList[groupIdx]),'html.parser')

                valueDict = self.getGroupData(groupSoup,dataDict[dataName])

                detailsDict[dataName] = valueDict

                groupIdx += 1

            weatherDict[dateDay.strftime('%d_%m_%Y')] = detailsDict

        return weatherDict
     

    def getGroupData(self,groupSoup,classList):
        groupDataDict = dict()
        if not classList:
            data = re.sub("\n","",groupSoup.get_text())
            groupDataDict["snowLine"] = data
        else:
            for className in classList:
                if className == "wgew":
                    dataRaw = groupSoup.find("span",class_=className)
                else:
                    dataRaw = groupSoup.find("div",class_=className)
                # filter new line character
                data = re.sub("\n","",dataRaw.get_text())
                groupDataDict[className] = data
        return groupDataDict


resortsList = ["diedamskopf","mellau"]
rootUrl = "https://www.bergfex.at/"
postFixUrl = "/wetter/prognose"
outFile = "weatherData.json"

oHandleRequest = handleRequest(resortsList,rootUrl,postFixUrl)
weatherData = oHandleRequest.getWeatherDataList()

with open(outFile, 'w') as outfile:
    json.dump(weatherData, outfile)

