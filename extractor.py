import itertools
import re
from parse import *

from google.cloud import translate_v2 as translate


def isMeasure(word):
    subStrings = []
    Measurement = ['mm','cm','m', 'ml','L','g','kg','°C']
    numbers = re.findall('[0-9]+', word)
    for number in numbers:
        index = int(word.find(number))
        length = int(len(number))
        subString = word[index+length: index+length+2]
        subStrings.append(subString)
        
    if any(unit in subStrings for unit in Measurement):
        return True
    else:
        return False

class Extractor:
    def __init__(self, itemID, OCRlist)-> list:
        self.itemID = itemID
        self.OCRlist = OCRlist
    
    def detect_lang(self):   
        
        contentDict = {}
        translate_client = translate.Client()
        for index, word in enumerate(self.OCRlist):
            result = translate_client.detect_language(word)
            langTag = result["language"]

            if langTag == 'zh-TW' or langTag == 'zh-CN':
                langTag = 'ja'
            contentDict[word] = index, langTag
        return contentDict

    def indexMatch(self):
        self.itemID = self.itemID.replace('s','').replace('_1','').strip()
        id_index = 0
        filter_object = filter(lambda x: 'ITEM#' in x, self.OCRlist)
        filter_ITEM = list(filter_object)[0]
        
        detect_ID = parse('ITEM# {}',filter_ITEM).fixed[0].strip()
        id_index = self.OCRlist.index(filter_ITEM)
                
        assert self.itemID in detect_ID, "Item ID doesn't match!"
        return id_index


    def indexSlice(self):
        contentDict = self.detect_lang()
        id_index = self.indexMatch()

        jpEnd_index = price_index = period_index = 0
        
        YenMark = ['¥', '羊', '半', '辛', '価格']
        try:
            price_match = [text for text in self.OCRlist if any(currency in text for currency in YenMark)][0]
            price_index = self.OCRlist.index(price_match)
        except:
            price_index = id_index

        for text in reversed(self.OCRlist):
            if '/' in text or '販売' in text:
                period_index = self.OCRlist.index(text)
                break
        
        nameDict = dict(itertools.islice(contentDict.items(), 0, price_index))
        
        for text, info in reversed(nameDict.items()):
            index, langTag = info
            if langTag != 'ja' and isMeasure(text) == True:
                jpEnd_index = index
                break
            elif langTag == 'ja':
                jpEnd_index = index
                break

        return jpEnd_index, price_index, period_index
        
    def price(self):
        jpEnd_index, price_index, period_index = self.indexSlice()
        priceTag = self.OCRlist[price_index]
        priceTag = priceTag.replace('半','¥').replace('辛','¥').replace('Y', '¥').replace('羊','¥').replace('率','¥')        
        price = priceTag
        return price       
    
    def jpName(self):
        jpEnd_index, _, _ = self.indexSlice()
        jpName = ' '.join(self.OCRlist[0:jpEnd_index+1])
        return jpName
    
    def enName(self):
        jpEnd_index, price_index, _ = self.indexSlice()
        enName = ' '.join(self.OCRlist[jpEnd_index+1: price_index])
        return enName
        
    def period(self):
        _, _, period_index = self.indexSlice()
        period = self.OCRlist[period_index]
        try:
            period = period.replace('|','')
        except:
            None
            
        return period
    
    def description(self):
        contentDict = self.detect_lang()
        _, price_index, period_index = self.indexSlice()
        description = ' '.join(list(dict(itertools.islice(contentDict.items(), price_index+1, period_index-1)).keys()))
        if len(description) == 0:
            description = 'No description'
        return description

    def itemInfo(self):
        price = self.price()
        jpName = self.jpName()
        enName = self.enName()
        period = self.period()
        description = self.description()
        
        return jpName,enName,price,period,description
    
    def __str__(self):
        jpName,enName,price,period,description = self.itemInfo()
        return "jpName: {}\nenName: {}\nPrice: {}\nPeriod: {}\nDescription: {}\n\n\n".format(jpName,enName,price,period,description)

