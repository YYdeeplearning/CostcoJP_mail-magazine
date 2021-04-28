import csv
import json
# import demjson


class Recorder:
    def __init__(self, discount_date, record_dict) -> dict:
        self.record_dict = record_dict
        self.discount_date = discount_date

        pass

    def record_json(self):
        with open('Costco_{}.json'.format(self.discount_date[-4:]), 'a+', encoding='utf-8') as file_json_dict:
            for itemID,itemInfo in self.record_dict.items():
                jpName,enName,price,period,description = itemInfo
                json.dump({self.discount_date:{'itemID':itemID,'itemName(JP)':jpName,'itemName(EN)':enName,'Price':price,'Period':period,'Description':description}}, file_json_dict, ensure_ascii=False, indent = 4)        
        print('Write into local json file Complete!')


    def record_csv(self):
        
        
        print('Write into local csv file Complete!')
        pass

    def record_allVersion(self):
        self.record_csv()
        self.record_json()