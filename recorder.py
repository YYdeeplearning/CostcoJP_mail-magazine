import json
import os
import pandas as pd



class Recorder:
    def __init__(self, discount_date, record_dict) -> dict:
        self.record_dict = record_dict
        self.discount_date = discount_date


    def path_setting(self, filetype) -> str:
        year = self.discount_date[-4:]
        try:
            os.chdir('Costco_{}/{}'.format(year, filetype))
        except:
            os.makedirs('Costco_{}/{}'.format(year, filetype))
            os.chdir('Costco_{}/{}'.format(year, filetype))


    def record_json(self):
        with open('{}_json.json'.format(self.discount_date.replace('/', '-')), 'w', encoding='utf-8') as file_json_dict:
            for itemID,itemInfo in self.record_dict.items():
                jpName,enName,price,period,description = itemInfo
                json.dump({self.discount_date:{'itemID':itemID,'itemName(JP)':jpName,'itemName(EN)':enName,'Price':price,'Period':period,'Description':description}}, file_json_dict, ensure_ascii=False, indent = 4)        
        print('Write into local json file Complete!')


    def record_excel(self):
        excel_list = []
        for itemID,itemInfo in self.record_dict.items():
            jpName,enName,price,period,description = itemInfo
            excel_dict = {'itemID':itemID,'itemName(JP)':jpName,'itemName(EN)':enName,'Price':price,'Period':period,'Description':description}
            excel_list.append(excel_dict)
        
        data_df = pd.DataFrame(excel_list)
        data_df.to_excel('{}_excel.xlsx'.format(self.discount_date.replace('/', '-')), index=False)
        
        print('Write into local excel file Complete!')


    def record_allVersion(self):
        self.record_json()
        self.record_excel()