import requests
# from html.parser import HTMLParser
from bs4 import BeautifulSoup
import datetime
import re
import json


class handleBergfexRequest:

    rootUrl = "https://www.bergfex.at/"
    postFixUrl = "/wetter/prognose"

    def getWeatherDataList(self,resortList):
        weatherDataDict = dict()
        # iterate over all resorts
        for resort in resortList:
            resortInfoDict = self.getWeatherData(resort)
            weatherDataDict[resort] = resortInfoDict

        # return weather dict
        return weatherDataDict

    def getWeatherData(self,resort):

        # create complete url
        resortUrl = self.rootUrl + resort + self.postFixUrl
        request = requests.get(url = resortUrl)
        # beautiful soup to parse html
        resortSoup = BeautifulSoup(request.text, 'html.parser')

        # get altitude
        elevationDict = dict()
        elevationDict["top"] = self.getAltitude("label-berg",resortSoup)
        elevationDict["bottom"] = self.getAltitude("label-tal",resortSoup)

        # get todays date
        date = datetime.datetime.now()

        # initialize weather dict
        weatherDict = dict()

        for day in range(9):
            
            # date of day
            dateDay = date + datetime.timedelta(days=day)
            
            # values of keys represent div tags with class = <value>
            dataDict = {
                "mountain " + elevationDict["top"]: ["tmax","tmin","nschnee"],
                "valley " + elevationDict["bottom"]: ["tmax","tmin","nschnee"],
                "rainProb": ["rrp"],
                "rainAmountSun": ["rrr","sonne"],
                "snowLine": [],
                "storm": ["wgew"],
                "wind": ["ff"]
            }

            # get day forcast string
            idStr = "forecast-day-" + str(day)
            forecastDayRaw = resortSoup.find("div", id=idStr)
            forecastDayRawSoup = BeautifulSoup(str(forecastDayRaw), 'html.parser')

            # get all div tags with class = "group*"
            groupRawList = forecastDayRawSoup.find_all("div",class_="group")
            groupIdx = 0

            # init weather day dictionary
            detailsDict = dict()

            for dataName in dataDict:

                groupSoup = BeautifulSoup(str(groupRawList[groupIdx]),'html.parser')

                # parse group html tag, to get values
                valueDict = self.getGroupData(groupSoup,dataDict[dataName])
                detailsDict[dataName] = valueDict
                groupIdx += 1

            weatherDict[dateDay.strftime('%d_%m_%Y')] = detailsDict

        return weatherDict


    def getAltitude(self,className,soup):
        divRaw = soup.find("div", class_=className)
        divRawSoup = BeautifulSoup(str(divRaw), 'html.parser')
        elevationRaw = divRawSoup.find("div", class_="elevation")
        elevation = re.sub(".","",elevationRaw.get_text())
        return elevation
     

    def getGroupData(self,groupSoup,classList):

        groupDataDict = dict()
        # snowline is organized differently
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

class handleWetterringRequest:

    rootUrl = "https://wetterring.at/wetterstationen/detail/"

    def getWeatherStationDataList(self,stationList):
        stationDetailDict = dict()
        for station in stationList:
            stationDetailDict[station] = self.getStationDetails(station)

        return stationDetailDict

    def getStationDetails(self, station):
        
        stationUrl = self.rootUrl + "/" + station
        request = requests.get(url = stationUrl)
        # beautiful soup to parse html
        stationSoup = BeautifulSoup(request.text, 'html.parser')

        dataIdBasis = "237"

        descDataId = ["temp","rainfall","","wind","humidity","","airPressure","",""]
        regeexpList = [
            "(-\d\d,\d|-\d,\d|\d,\d|\d\d,\d)",
            "(\d*,\d*|--)",
            "",
            "(\d,\d|\d\d,\d|\d\d\d,\d)",
            "(\d\d)",
            "",
            "(\d.\d\d\d|--)",
            "",
            "",
            ]

        dataIdDict = dict()

        for dataIdIdx in range(9):

            if descDataId[dataIdIdx]:
                dataId = dataIdBasis + str(dataIdIdx + 1)   
                dataRaw = stationSoup.find("div", attrs={"data-id": dataId})

                dataRawSoup = BeautifulSoup(str(dataRaw),'html.parser')

                groupDict = dict()
                
                currentHeaderRaw = dataRawSoup.find("div", class_="fallback-title").get_text()
                currentHeader = re.findall(regeexpList[dataIdIdx], currentHeaderRaw)[0]

                groupDict["curr"+descDataId[dataIdIdx]] = currentHeader

                groupRawList = dataRawSoup.find_all("div", class_="row")

                descListGroup = ["dayMax","dayMin","monthMax","monthMin","yearMax","yearMin"]
                
                groupIdx = 0
                for groupRaw in groupRawList:

                    valueDict = dict()
                    groupSoup = BeautifulSoup(str(groupRaw),'html.parser')

                    groupDataRawList = groupSoup.find_all("div",class_=re.compile("col\w*"))

                    dataIdx = 0
                    descListData = ["value","","desc","time"]

                    for dataRaw in groupDataRawList:
                        if descListData[dataIdx] and descListData[dataIdx] != "desc":
                            valueDict[descListData[dataIdx]] = dataRaw.get_text()
                        dataIdx += 1
                    
                    groupDict[descListGroup[groupIdx]] = valueDict
                    groupIdx += 1
                
                dataIdDict[descDataId[dataIdIdx]] = groupDict
            
        return dataIdDict
