# import validator
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
    # assert validator.url(site) == True, "Please input correct url!"
        

    Costco_collector = Collector(site)
    itemDict = Costco_collector.collectItem()
    discountDate = Costco_collector.collectDate()

    record_dict = {}
    for itemID, url in itemDict.items():
        Costco_processor = Processor(itemID, url)
        textList = Costco_processor.detect_text()
        Costco_extractor = Extractor(textList)
        result = Costco_extractor.itemInfo()
        record_dict[itemID.replace('s','').replace('_1','')] = result
        break

    Costco_recorder = Recorder(discountDate, record_dict )
    Costco_recorder.record_json()


if __name__ == "__main__":
    main()


