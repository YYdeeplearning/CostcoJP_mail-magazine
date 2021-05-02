import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


class Collector:
    def __init__(self, site) -> str:
        self.site = site

    def collectItem(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

        response = requests.get(self.site, headers=headers)
        html = response.content

        soup = BeautifulSoup(html,'lxml')
        imgList = soup.find_all('img')

        itemDict = {}

        for imgUrl in imgList[:]:
            itemlink = imgUrl.get('src')
            itemID = itemlink.split('/')[-1].replace('.jpg','')
            if itemID.startswith('s') == True and itemID.startswith('sk') == False:
                itemDict[itemID] = itemlink

        for itemID in list(itemDict.keys()):
            if itemID.endswith('_1') == True:
                del itemDict[itemID.replace('_1','')]
        
        return itemDict
    
    def collectDate(self):
        siteList = self.site.split('/')
        date_abbr = re.findall(r'\d+', siteList[6])[0]
        date = '20' + date_abbr
        date = datetime.strptime(date, '%Y%m%d').strftime('%m/%d/%Y')

        return date

    def __str__(self):
        itemDict = self.collectItem()
        date = self.collectDate(self)
        return "Date: {}\nitemDict:\n {}\n".format(date, itemDict)