import os

from collector import Collector
from extractor import Extractor
from processor import Processor
from recorder import Recorder


__author__ =  "YU Yang"

def main():

    os.chdir(os.getcwd())
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "Google_Service_API.json"

    site = input("Please paste Costco link here: ")

    Costco_collector = Collector(site)
    itemDict = Costco_collector.collectItem()
    discount_date = Costco_collector.collectDate()

    record_dict = {}
    for itemID, url in itemDict.items():
        Costco_processor = Processor(itemID, url)
        textList = Costco_processor.detect_text()
        Costco_extractor = Extractor(itemID, textList)
        result = Costco_extractor.itemInfo()
        record_dict[itemID.replace('s','').replace('_1','')] = result
        # break

    Costco_recorder = Recorder(discount_date, record_dict)
    
    try:
        os.chdir('Costco_{}'.format(discount_date[-4:]))
    except:
        os.mkdir('Costco_{}'.format(discount_date[-4:]))
        os.chdir('Costco_{}'.format(discount_date[-4:]))

    Costco_recorder.record_allVersion()
    


if __name__ == "__main__":
    main()


