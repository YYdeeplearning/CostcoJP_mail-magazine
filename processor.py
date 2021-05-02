import io
from PIL import Image
import requests


from google.cloud import vision

class Processor:
    def __init__(self, itemID, url) -> str:
        self.itemID = itemID
        self.url = url

    def detect_text(self):
        """Detects text in the file."""

        img = Image.open(requests.get(self.url, stream=True).raw)
        if self.itemID.endswith('_1') == False:
            img_width, img_height = img.size
            img_crop = img.crop((0, img_height//2, img_width,img_height))
        else:
            img_crop = img
        
        img_bytes = io.BytesIO()
        img_crop.save(img_bytes, format='jpeg')
        img_bytes = img_bytes.getvalue()
        
        client = vision.ImageAnnotatorClient()

        image = vision.Image(content = img_bytes)

        response = client.text_detection(image = image)
        texts = response.text_annotations
        text = texts[0].description
        text = text.strip()
        textList = text.split('\n')
        
        return textList

    def __str__(self) -> str:
        textList = self.detect_text()
        return 'OCR Result:{}'.format(textList)
