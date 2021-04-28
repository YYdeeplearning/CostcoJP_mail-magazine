# CostcoJP_mail-magazine (Beta version)
These are scripts that can scrape, extract and store mail-magazine information from Costco Japan since January 2021.

![51211314855966](https://user-images.githubusercontent.com/30718867/115746621-6e5bcd80-a3cf-11eb-9873-0b152ce30d2b.jpg)

Attention! The entire scripts only work for Costco Japan!


## Requirements
- Python 3.8.5 64-bit
- Validator
- BeautifulSoup
- Cloud Translation - Basic (v2)
- Cloud Vision API 
- PIL
- lxml


Use the package manager pip to install cloud-vision and cloud-translate:
  ```bash
  pip install validator
  pip install beautifulsoup4
  pip install google-cloud-vision
  pip install google-cloud-translate
  pip install Pillow
  pip install lxml
  ```

## Usage
1. To run this program, you need to first set your own Cloud Vision API & Cloud Translation - Basic (v2) API. Plesae refer these two guides:
   * Cloud Translation: https://cloud.google.com/translate/docs/setup
   * Cloud Vision: https://cloud.google.com/vision/docs/setup
2. Download the json file as API key and put into Root directory with renaming as "Google_Service_API.json"
3. Run "main.py" and paste the Costco mail-magazine link, such as: https://cds.costcojapan.jp/cds/mail-images/upz/210422_rr8e/thu22d/pc_index.html when required input the link.
4. The result of json file can be found at root directory.


## Future Work
1. Add more comments into program
2. Add .csv file as output
3. Modify recorder.py like use mkdir() to creat directory 
4. Optimize Readme.md
