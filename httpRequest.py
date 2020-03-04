import requests
# from html.parser import HTMLParser
from bs4 import BeautifulSoup


# urlDiedamskopf = 'https://www.bergfex.at/diedamskopf/wetter/berg/'
urlDiedamskopf = 'https://www.bergfex.at/diedamskopf/wetter/prognose/#day0'
forecastFile = 'forecast.html'

# make https request to get html data
r = requests.get(url = urlDiedamskopf)

soup = BeautifulSoup(r.text, 'html.parser')

forecastList = soup.find_all("div", class_="interval")

fId = open(forecastFile,'w')

forecastDay0 = soup.find("div", id="forecast-day-0-intervals")
forecastDay0Soup = BeautifulSoup(str(forecastDay0),'html.parser')
forecastDay0IntervalList = forecastDay0Soup.find_all("div", class_="interval")

tmpList = []
newSnowList = []
# for interval in forecastDay0IntervalList:
interval = forecastDay0IntervalList[0]
intervalSoup = BeautifulSoup(str(interval),'html.parser')
# temperatur
tmaxRawList = intervalSoup.find_all("div",class_="tmax")
for tmax in tmaxRawList:
    tmpList.append(tmax.get_text())
# neuschnee
newSnowRawList = intervalSoup.find_all("div", class_="nschnee")
for newSnow in newSnowRawList:
    newSnowList.append(newSnow.get_text())
# sonnenschein
sunRaw = intervalSoup.find("div", class_="sonne")
sun = sunRaw.get('class')[1]
# regenmenge
rainfallRaw = intervalSoup.find("div", class_="rrr")
rainfall = rainfallRaw.get_text()
# regenwahrscheinlichkeit
rainfallProbRaw = intervalSoup.find("div", class_="rrp")
rainfallProb = rainfallProbRaw.get_text()
# schneefallgrenze
snowLineRaw = intervalSoup.find("div", class_="group sgrenze")
snowLine = snowLineRaw.get_text()
# gewitterwahrscheinlichkeit
stormRaw = intervalSoup.find("div", class_="group wgew ")
storm = stormRaw.get_text()
# windstärke
windForceRaw = intervalSoup.find("div", class_="ff ff0")
windForce = windForceRaw.get_text()
# windgeschwindigkeit
windSpeedRaw = intervalSoup.find("div", class_="ff ff0 ff-kmh")
windSpeed = windSpeedRaw.get_text()






for forecast in forecastList:
    fId.write(str(forecast))
# forecast1dHtml = soup.find_all("div",class_ ="interval fields")
# forecast9dHtml = soup.find('div','forecast9d-container touch-scroll-x')

# # write data to file
# fId.writelines([str(forecast1dHtml), str(forecast9dHtml)])
fId.close
