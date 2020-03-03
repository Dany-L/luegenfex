import requests
# from html.parser import HTMLParser
from bs4 import BeautifulSoup


urlDiedamskopf = 'https://www.bergfex.at/diedamskopf/wetter/berg/'
forecastFile = 'forecast.html'

# make https request to get html data
r = requests.get(url = urlDiedamskopf)

soup = BeautifulSoup(r.text, 'html.parser')

forecast1dHtml = soup.find('div','forecast1h-container')
forecast9dHtml = soup.find('div','forecast9d-container touch-scroll-x')

fId = open(forecastFile,'w')

# write data to file
fId.writelines([str(forecast1dHtml), str(forecast9dHtml)])
fId.close
